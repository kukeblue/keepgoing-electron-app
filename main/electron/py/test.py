# import logUtil
import pyautogui
import time

# pyautogui.FAILSAFE = False

# # def slowMove(x1, y1, x2, y2):
# #     points = []
# #     cx = (x2 - x1)/2 + 50 + x1
# #     cy = (y2 - y1)/2 + 50 + y1
# #     for index in range(4):
# #         point = getSlowMovePoint(0.25 * (index + 1), 0, 0, 1200, 0, cx, cy)
# #         points.append(point)
# #     for index in range(4):
# #         point = points[index]
# #         pyautogui.moveTo(point[0], point[1])

# # def getSlowMovePoint(t, x1, y1, x2, y2, cx, cy):
# #     x = int((1 - t) * (1 - t) * x1 + 2 * t * (1 - t) * cx + t * t * x2)
# #     y = int((1 - t) * (1 - t) * y1 + 2 * t * (1 - t) * cy + t * t * y2)
# #     return [x, y]

# import baiduApi
# # slowMove(1200, 500, 1900, 20)


# def init():
#     # need to run only once to download and load model into memory
#     img_path = './config/images/temp/temp_baotu_info.png'
#     baiduApi.F_通用文字识别(img_path)
# from paddleocr import PaddleOCR

# ocr=PaddleOCR(use_angle_cls = True,use_gpu= True)
# text=ocr.ocr("D:\develop\project\keepgoing-electron-app\main\electron\py\config\images/temp/temp_zuobiao_info.png",cls=True)

# #打印所有文本信息
# ret = ''
# while(True):
#     pyautogui.press('up')
#     pyautogui.press('enter')
#     time.sleep(10)
# for t in text:
#     ret = ret + t[1][0]
# print(ret)

import json

str = '[ [ 15, 20 ], [ 5, 28 ], [ 17, 150 ] ]'
data = json.loads(str)
print(data[0])
# if __name__ == "__main__":
