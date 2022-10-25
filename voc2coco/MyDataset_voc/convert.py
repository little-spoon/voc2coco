# coding:utf-8
# pip install lxml
# 参考博客链接为：https://blog.csdn.net/weixin_43878078/article/details/120578830
"""
convert.py
1. 建议按照以下层次放置数据集文件和本代码：
|--MyDataset_voc
    |--Annotations
        |--0001.xml
        |...
    |--JPEGImages
        |--0001.jpg
        |...
    |--convert.py
|--MyDataset_coco 新建文件夹，用于存放转换后的图片和json文件
    |--train 新建文件夹，用于存放训练集图片
    |--val 新建文件夹，用于存放验证集图片
    |--test 新建文件夹，用于存放测试集图片
如果你不是按照以上层次放置数据集，请自行修改对应文件的路径。
2. 在JPEFImages和Annotations中分别放入全部的图片和xml文件
3. 设置训练集、验证集、测试集比例
train_ratio = 0.8
val_ratio = 0.1
4. 修改类别 classes
"""
import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET

START_BOUNDING_BOX_ID = 1


def get(root, name):
    return root.findall(name)


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def convert(xml_list, json_file):
    json_dict = {"info": ['none'], "license": ['none'], "images": [], "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        # print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()

        filename = os.path.basename(xml_f)[:-4] + ".jpg"

        image_id = filename.split('.')[0][-4:]  # 图片的后四位
        #         print('filename is {}'.format(image_id))

        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id': image_id}
        json_dict['images'].append(image)
        ## Cruuently we do not support segmentation
        #  segmented = get_and_check(root, 'segmented', 1).text
        #  assert segmented == '0'
        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in all_categories:
                all_categories[category] += 1
            else:
                all_categories[category] = 1
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print(
                    "[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(
                        category, pre_define_categories, new_id))
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
            assert (xmax > xmin), "xmax <= xmin, {}".format(line)
            assert (ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width * o_height, 'iscrowd': 0, 'image_id':
                image_id, 'bbox': [xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'person', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))
    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories),
                                                                                  all_categories.keys(),
                                                                                  len(pre_define_categories),
                                                                                  pre_define_categories.keys()))
    print("category: id --> {}".format(categories))
    print(categories.keys())
    print(categories.values())


if __name__ == '__main__':
    # xml标注文件夹
    xml_dir = './Annotations'
    # 训练数据的josn文件
    save_json_train = '../MyDataset_coco//train.json'
    # 验证数据的josn文件
    save_json_val = '../MyDataset_coco/val.json'
    # 测试数据的test文件
    save_json_test = '../MyDataset_coco/test.json'
    # 类别，如果是多个类别，往classes中添加类别名字即可，比如['dog', 'person', 'cat']
    classes = []
    pre_define_categories = {}
    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i + 1
    print("pre_define_categories", pre_define_categories)
    only_care_pre_define_categories = True

    # 训练数据集比例，当这两个都填0的时候，测试集（test_ratio）就是1了
    train_ratio = 0.8
    val_ratio = 0.1
    print('xml_dir is {}'.format(xml_dir))
    xml_list = glob.glob(xml_dir + "/*.xml")
    images_list = glob.glob("./JPEGImages/*.jpg")
    xml_list = np.sort(xml_list)

    np.random.seed(100)
    np.random.shuffle(xml_list)

    train_num = int(len(xml_list) * train_ratio)
    val_num = int(len(xml_list) * val_ratio)
    print('训练样本数目是 {}'.format(train_num))
    print('验证样本数目是 {}'.format(val_num))
    print('测试样本数目是 {}'.format(len(xml_list) - train_num - val_num))
    xml_list_val = xml_list[:val_num]
    print("xml_list_val,", xml_list_val)
    xml_list_train = xml_list[val_num:train_num + val_num]
    print("xml_list_train,", xml_list_train)
    xml_list_test = xml_list[train_num + val_num:]
    print("xml_list_test,", xml_list_test)

    # 移动对应图片到对应的文件夹
    val_name_list = []
    train_name_list = []
    test_name_list = []
    val_name_list2 = []
    train_name_list2 = []
    test_name_list2 = []

    for name in xml_list_val:
        val_name_list.append(name[14:])  # 根据你的目录，你可能需要修改这里的数字，建议按照默认方式放置
    for i in range(len(val_name_list)):
        val_name_list[i] = val_name_list[i][:-4]  # 剪掉后四个元素，也就是.xml,得到图片的名称
    for name in xml_list_train:
        train_name_list.append(name[14:])  # 根据你的目录，你可能需要修改这里的数字，建议按照默认方式放置
    for i in range(len(train_name_list)):
        train_name_list[i] = train_name_list[i][:-4]  # 剪掉后四个元素，也就是.xml,得到图片的名称
    for name in xml_list_test:
        test_name_list.append(name[14:])  # 根据你的目录，你可能需要修改这里的数字，建议按照默认方式放置
    for i in range(len(test_name_list)):
        test_name_list[i] = test_name_list[i][:-4]  # 剪掉后四个元素，也就是.xml,得到图片的名称
    images_root_dir = "./JPEGImages/"
    images_name_list = os.listdir(images_root_dir)
    for i in range(len(images_name_list)):
        images_name_list[i] = images_name_list[i][:-4]
    print("images_name_list", images_name_list)

    for images_name in images_name_list:
        for val_name in val_name_list:
            if images_name == val_name:
                val_name_list2.append(images_name)
                source_path = images_root_dir + images_name + ".jpg"
                des_path = "../MyDataset_coco/val/" + val_name + ".jpg"
                shutil.move(source_path, des_path)
        for train_name in train_name_list:
            if images_name == train_name:
                train_name_list2.append(images_name)
                source_path = images_root_dir + images_name + ".jpg"
                des_path = "../MyDataset_coco/train/" + train_name + ".jpg"
                shutil.move(source_path, des_path)
        for test_name in test_name_list:
            if images_name == test_name:
                test_name_list2.append(images_name)
                source_path = images_root_dir + images_name + ".jpg"
                des_path = "../MyDataset_coco/test/" + test_name + ".jpg"
                shutil.move(source_path, des_path)

    print("val_pic,", val_name_list2)
    print("train_pic,", train_name_list2)
    print("test_pic,", test_name_list2)

    # 对训练数据集对应的xml进行coco转换
    convert(xml_list_train, save_json_train)
    # 对验证数据集的xml进行coco转换
    convert(xml_list_val, save_json_val)
    # 对测试数据集的xml进行coco转换
    convert(xml_list_test, save_json_test)
