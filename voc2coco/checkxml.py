# coding=utf-8
import os
from xml.etree.ElementTree import ElementTree, Element
'''checkxml.py'''
def read_xml(in_path):
    '''''读取并解析xml文件
    in_path: xml路径
    return: ElementTree'''
    tree = ElementTree()
    tree.parse(in_path)
    return tree

def check():
    url = "E:/annotations/"  # 修改成annotation的目录
    i = 0
    list_error = []
    for item in os.listdir(url):
        tree = read_xml(url + "/" + item)
        root = tree.getroot()
        object = root.findall("object")
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        if object == None:
            print(item)
            continue
        for it in object:
            bndbox = it.find("bndbox")
            if bndbox == None:
                print("bndbox == None")
                print(item)
            xmin = int(bndbox.find("xmin").text)
            xmax = int(bndbox.find("xmax").text)
            ymin = int(bndbox.find("ymin").text)
            ymax = int(bndbox.find("ymax").text)
            if xmin <= 0 or xmin >= xmax or ymin <= 0 or ymin >= ymax:
                # 本段注释的代码用于把xmin\xmax, ymin\ymax互换，以及把为0的xmin\ymin改成1，一般来说用不到
                # if xmin >= xmax:
                #     temp = xmin
                #     bndbox.find("xmin").text = str(xmax)
                #     bndbox.find("xmax").text = str(temp)
                # if ymin >= ymax:
                #     temp = ymin
                #     bndbox.find("ymin").text = str(ymax)
                #     bndbox.find("ymax").text = str(temp)
                # if xmin == 0:
                #     bndbox.find("xmin").text = str(1)
                # if ymin == 0:
                #     bndbox.find("ymin").text = str(1)
                # tree.write("E:/annotations_update/"+item)
                print("xmin <= 0 or xmin >= xmax or ymin <=0 or ymin >= ymax", xmin, ymin) # 定位到出错的具体位置，在xml中搜索xmin或ymin的具体数据即可
                print(item)
                list_error.append(item)
                i += 1
            if xmax > width or ymax > height:
                print("xmax > width or ymax> height",xmin,ymax)
                print(item)
                list_error.append(item)
                i += 1
    print(list(set(list_error)))
    print(len(list(set(list_error))))

if __name__ == '__main__':
    check()
