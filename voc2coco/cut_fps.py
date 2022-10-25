import cv2
import os

'''
cut_fps.py
你可能需要修改的变量：
path: 视频路径
path_to_save: 截取图片保存的路径
frameRate: 帧数截取间隔
注意：
1. 修改路径请不要忘记添加最后一个/
2. 请不要把保存图片的文件夹放在视频所在文件夹下
3. 如果视频时长大于10分钟，代码可能失效，需要把长视频切成短视频后使用
'''
path = "E:/myvideo/"
path_to_save = "E:/save/"

files = os.listdir(path)
cap = cv2.VideoCapture(path + files[0])
for i in range(len(files)):
    files[i] = files[i][:-4]  # 这是为了仅获得视频的名称，去掉.mp4
print("获取视频名称列表：", files)

c = 1
frameRate = 125  # 帧数截取间隔（每隔125帧截取一帧）
num_video = 0
while (True):
    ret, frame = cap.read()
    if ret:
        if (c % frameRate == 0):
            print("开始截取视频第：" + str(c) + " 帧")
            cv2.imwrite(path_to_save + files[num_video] + "_" + str(c) + '.jpg', frame)  # 这里是将截取的图像保存在path_to_save
        c += 1
        cv2.waitKey(0)
    else:
        print("第" + str(num_video + 1) + "个视频" + "所有帧都已经保存完成")
        if num_video == len(files) - 1:
            break
        else:
            num_video += 1
            next_file = path + files[num_video] + ".mp4"
            cap = cv2.VideoCapture(next_file)
            c = 1
cap.release()
