# 用于批量重命名文件名，在文件名后面加上0000~9999的编号
import os
source_dir='E:/myvideo/' # 原路径
dest_dir='E:/myvideo/'# 重命名后的存放路径
f=os.listdir(source_dir)

for i in range(len(f)):
    os.rename((source_dir+f[i]),(dest_dir + f[i][:-4]+ f'{i:04}' + '.jpg'))# 如果是重命名图片就是.jpg，重命名xml图片需要改成.xml
    print(dest_dir + f[i][:-4]+ f'{i:04}' + '.jpg')
print("done")

