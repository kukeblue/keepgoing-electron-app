# coding=utf-8
from aip import AipOcr
import time
from win32com.client import Dispatch
from cnocr import CnOcr
import win32api
import sys
import os
import logUtil
import pyautogui

# import easyocr
# reader = easyocr.Reader(['ch_sim', 'en'])
ocr = CnOcr()

op = Dispatch("op.opsoft")

pyHome = __file__.strip('baiduApi.pyc')
pyZhikuDir = pyHome + 'config\zhiku'
pyZhikuDir2 = pyHome + 'config\images'

APP_ID = '25713120'
API_KEY = 'GOkNrLxVH3cV8I7DVpXx67mh'
SECRET_KEY = '9MTEeMd2nNcm457CsGTGNV5ddkISAuI1'
client = None
with open(pyZhikuDir2 + '\\temp\\913.txt', "r", encoding='utf-8') as f:
    data = f.read()
    textAppData = data.split(',')
    f.close()
    client = AipOcr('28169102', 'TlqWuTLLPyVnoMAILQQnhQU1',
                    '3T2wyhRHS7pH7euXSefHRR6gjcE1h1I2')

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


options = {"language_type": "CHN_ENG", "detect_direction": "false",
           "detect_language": "false", "probability": "false"}


def getImageText(path):
    image = get_file_content(path)
    return client.basicAccurate(image, options)


def F_通用文字识别(path, area):
    baiduRetStr = getImageText(path)
    str = ''
    for item in baiduRetStr['words_result']:
        str = str + item['words']
    print(str)
    return str


def F_大漠宝图文字识别(area):
    op.SetDict(0, pyZhikuDir + '\\baotuzuobiao.txt')
    str = op.Ocr(area[0], area[1], area[2], area[3],
                 "00ff00-000000", 0.98)
    return str


def F_大漠红色文字位置识别(area, text):
    op.SetDict(0, pyZhikuDir + '\\red.txt')
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     text, "ff0000-000000", 0.8)
    if(ret[0] > -1):
        return [ret[1], ret[2]]


def F_大漠红色4小人弹框识别(area):
    op.SetDict(0, pyZhikuDir + '\\4p.txt')
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     '锟斤拷', "ffffff-000000", 0.8)
    print(ret)
    if(ret[0] > -1):
        return [ret[1], ret[2]]


def F_小地图出入口按钮识别(area):
    op.SetDict(0, pyZhikuDir + '\\map_intro.txt')
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     '1', "e706eb-000000|e706eb-000000|bc05bf-000000|ff01ff-000000|b013be-000000|e302e5-000000", 0.6)
    print(ret)
    if(ret[0] > -1):
        return [ret[1], ret[2]]


def F_打图4小人识别(area):
    for x in range(2):
        op.SetDict(0, pyZhikuDir + '\\baise.txt')
        ret = op.FindStr(area[0], area[1], area[2], area[3],
                         'qxz', "ffffff-000000", 0.6)
        print(ret)
        if(ret[0] > -1):
            return [ret[1], ret[2]]
    for x in range(2):
        op.SetDict(0, pyZhikuDir + '\\baise.txt')
        ret = op.FindStr(area[0], area[1], area[2], area[3],
                         'gxn', "ffffff-000000", 0.6)
        print(ret)
        if(ret[0] > -1):
            return [ret[1], ret[2]]


def F_大鬼小鬼任务区间识别(area):
    data = {
        '鬼王': None,
        '捉鬼': None,
    }
    op.SetDict(0, pyZhikuDir + '\\renwu_green.txt')
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     '鬼王', "00ff00-000000", 0.7)
    if(ret[0] > -1):
        data['鬼王'] = [ret[1]-20, ret[2]-20, 166, 99]
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     '捉鬼', "00ff00-000000", 0.7)
    if(ret[0] > -1):
        data['捉鬼'] = [ret[1]-20, ret[2]-20, 183, 110]
    return data


def F_人物位置识别(area):
    ret = op.FindMultiColor(area[0], area[1], area[2], area[3], 'f8fcf8',
                            '1|-1|f870f8,2|1|f850f8,38|-171|ff01ff,10|-1|80a818', 0.56, 0)
    if(ret[0] == 1):
        return [ret[0] + 33, ret[1] - 120]


def F_大漠小地图寻路坐标识别(area):
    op.SetDict(0, pyZhikuDir + '\\zuobiao_map.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffff00-000000", 1.0)

    return ret


def F_大漠摄妖香分钟识别(area):
    op.SetDict(0, pyZhikuDir + '\\syx_number.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffffff-000000", 1.0)
    return ret


def F_大漠小地图识别(area):
    op.SetDict(0, pyZhikuDir + '\\small_map.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffffff-000000", 0.85)
    return ret


def F_查找等级(area):
    op.SetDict(0, pyZhikuDir + '\\yellow.txt')
    ret = op.FindStr(area[0], area[1], area[2], area[3],
                     'dengji', "fefe00-000000|ffff00-000000", 0.75)
    if(ret[0] > -1):
        ret = op.Ocr(ret[1] + 25, ret[2], ret[1] + 50, ret[2] + 15,
                     "fefe00-000000|ffff00-000000", 0.75)
        return ret
    else:
        return ''


def cnocr文字识别2(path):
    res = ocr.ocr_for_single_line(path)
    print(res)
    if 'text' in res:
        print(res['text'])
    else:
        return ''.join(str(i) for i in res[0]) 
    # return ''


def cnocr文字识别(path):
    # res = reader.readtext(path)
    # if(len(res) == 0):
    #     return ""
    # return res[0][1]
    return ''

    # def F_识别放生验证数字(area):
    #     op.SetDict(0, pyZhikuDir + '\\fangshen_number.txt')
    #     return op.Ocr(area[0], area[1], area[2], area[3],
    #                   "eff104-000000|ffff01-000000|ffff01-000000|dee109-000000|ffff01-000000|c5cb0f-000000", 0.8)


def F_大漠坐标文字识别(area):
    op.SetDict(0, pyZhikuDir + '\\zuobiao.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffffff-000000|f8f8f8-000000", 1.0)
    print(ret)
    return ret


# ======================== 碗子山巡逻识别 ===============================
# region = (0, 0, 800, 600)
# def F_碗子山_蝎子():
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-xz-1.png', confidence=0.7, region=region)
#     if(point != None):
#         return point
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-xz-2.png', confidence=0.7, region=region)
#     if(point != None):
#         return point
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-xz-3.png', confidence=0.7, region=region)
#     if(point != None):
#         return point
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-xz-4.png', confidence=0.7, region=region)
#     if(point != None):
#         return point
   
   
    
# def F_碗子山_猫():
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-mm-1.png', confidence=0.7, region=region)
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-mm-4.png', confidence=0.7, region=region)
#     print(point)
#     print()
    
# def F_碗子山_混沌():
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-hd-4.png', confidence=0.7, region=region)
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-hd-3.png', confidence=0.7, region=region)
#     print(point)
    
# def F_碗子山_葫芦():
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-hl-1.png', confidence=0.7, region=region)
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-hl-4.png', confidence=0.7, region=region)
#     print(point)

# def F_碗子山_豹子():  
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-kb-2.png', confidence=0.7, region=region)
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-kb-4.png', confidence=0.7, region=region)
#     point = pyautogui.locateOnScreen(pyZhikuDir2 + '\\' + 'all-wzs-kb-1.png', confidence=0.7, region=region)
#     print(point)

# print(F_碗子山_混沌())