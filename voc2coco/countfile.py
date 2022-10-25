import os
path = "./annotations" # 要计数的文件夹路径
count = 0
for file in os.listdir(path):  # file 表示的是文件名
    count = count + 1
print(count)
#E:/notinlinevideo/annotations2
#E:/mydataset162voc/cut
