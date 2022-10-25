import numpy as np
import cv2
import os
import time

'''
cut_video.py
你需要修改的变量：
video: 视频路径
video_to_save: 截取图片保存前缀
size: 视频分辨率
MID_HOUR,MID_MIN,MID_SECOND: 从视频中间切割时间的 时 分 秒
END_HOUR,END_MIN,END_SECOND: 结束切割时间的 时 分 秒
注意：
1. 请不要把保存切割视频的文件夹放在原视频所在文件夹下
2. 由于可能每个视频的时长不一样，这份代码一次只能处理一个视频，如果需要批量处理，请参考cut_fps.py进行修改
'''

# 将视频切割成更小的视频
START_HOUR = 0
START_MIN = 0
START_SECOND = 0
START_TIME = START_HOUR * 3600 + START_MIN * 60 + START_SECOND  # 设置开始时间(单位秒)
MID_HOUR = 0
MID_MIN = 0
MID_SECOND = 15
MID_TIME = MID_HOUR * 3600 + MID_MIN * 60 + MID_SECOND  # 设置切割位置时间(单位秒)
END_HOUR = 0
END_MIN = 0
END_SECOND = 38
END_TIME = END_HOUR * 3600 + END_MIN * 60 + END_SECOND  # 设置结束时间(单位秒)

video = "E:/myvideo/MyVideo_1.mp4"
video_to_save="E:/save/MyVideo_1"  # 不需要加上.mp4，在后面保存的时候会加上
cap = cv2.VideoCapture(video)
FPS = cap.get(cv2.CAP_PROP_FPS)
print(FPS)
size = (1280, 720)
print(size)
TOTAL_FRAME = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 获取视频总帧数

frameToStart = START_TIME * FPS  # 开始帧 = 开始时间*帧率
print(frameToStart)
frametoMid = MID_TIME * FPS  # 中间帧 = 结束时间*帧率
print(frametoMid)
frametoStop = END_TIME * FPS  # 结束帧 = 结束时间*帧率
print(frametoStop)

videoWriter = cv2.VideoWriter(video_to_save+"a.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                              FPS, size)
videoWriter2 = cv2.VideoWriter(video_to_save+"b.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                               FPS, size)
COUNT = 0
while True:
    success, frame = cap.read()
    if success:
        COUNT += 1
        if COUNT <= frametoMid and COUNT > frameToStart:  # 选取起始帧
            print('correct= ', COUNT)
            videoWriter.write(frame)
        elif COUNT <= frametoStop and COUNT > frametoMid:
            videoWriter2.write(frame)
    if COUNT > frametoStop:
        print("结束")
        break
print('end')
