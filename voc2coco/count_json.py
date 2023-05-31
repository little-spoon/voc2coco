import json
# 打开你要计算的标注文件
with open('E:/annotations.json','r') as file:
    data=json.load(file)
    #你可以通过在线的JSON可视化工具(https://www.bejson.com/jsonviewernew/)查看当前JSON文件的格式
    #以COCO数据集为例，他的格式为:
    '''
    -JSON
        -info
        -licenses
        -images
            -... 略写
        -annotations
            -... 略写
        -categories
            -... 略写
    下面写了一些获取信息的例子，主要就是根据这个数据结构来获取相关的信息，所以看清楚数据结构很重要
    '''
    # 1. 通过images可以获得常用信息
    len_images=len(data['images'])# 图片数量
    # 遍历图像
    for i in range(len_images):
        images_name=data['images'][i]['file_name']# 当前图片的名称
        images_height=data['images'][i]['height']# 当前图片的高
        images_width = data['images'][i]['width']# 当前图片的宽

    # 2. 通过annotations可以获得的常用信息
    len_annotations=len(data['annotations'])# 标注数量
    # 遍历标注
    for i in range(len_annotations):
        anno_area=data['annotations'][i]['area'] # 当前标注的像素个数（绝对大小）
        anno_category_id=data['annotations'][i]['category_id']# 当前像素所属类别
        anno_bbox=data['annotations'][i]['bbox'] # 标注框的信息 里面包含四个值(x,y,w,h)
    # 你可以通过以上信息自行计算一些值，例如标注的平均大小、标注的密度、标注大小的分布情况等等

