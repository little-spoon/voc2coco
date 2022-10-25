from pycocotools.coco import COCO

annFile ='E:/annotations/train.json' # 要统计的json文件
# initialize COCO api for instance annotations
coco_train = COCO(annFile)

# display COCO categories and supercategories
# 显示所有类别
cats = coco_train.loadCats(coco_train.getCatIds())
cat_nms = [cat['name'] for cat in cats]
print('COCO categories:\n{}'.format('\n'.join(cat_nms)) + '\n')

for catId in coco_train.getCatIds():
    imgId=coco_train.getImgIds(catIds=catId)
    annId=coco_train.getAnnIds(catIds=catId)
    print("{:<6} {:<6d} {:<10d}".format(catId,len(imgId),len(annId)))

print("NUM_categories： " + str(len(coco_train.dataset['categories'])))
print("NUM_images: " + str(len(coco_train.dataset['images'])))
print("NUM_annotations: " + str(len(coco_train.dataset['annotations'])))