# coding=utf-8
from aip import AipOcr
import time
from win32com.client import Dispatch
import win32api
import utils
import sys
import os
import logUtil
op = Dispatch("op.opsoft")

pyHome = __file__.strip('baiduApi.py')
pyZhikuDir = pyHome + 'config\zhiku'


APP_ID = '25713120'
API_KEY = 'GOkNrLxVH3cV8I7DVpXx67mh'
SECRET_KEY = '9MTEeMd2nNcm457CsGTGNV5ddkISAuI1'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

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
                     text, "ff0000-000000", 1.0)
    if(ret[0] > -1):
        return [ret[1], ret[2]]


def F_大漠小地图识别(area):
    op.SetDict(0, pyZhikuDir + '\\small_map.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffffff-000000", 1.0)
    print(ret)
    return ret


def F_大漠小地图寻路坐标识别(area):
    op.SetDict(0, pyZhikuDir + '\\zuobiao_map.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffff00-000000", 1.0)
    print(ret)
    return ret


def F_大漠坐标文字识别(area):
    op.SetDict(0, pyZhikuDir + '\\zuobiao.txt')
    ret = op.Ocr(area[0], area[1], area[2], area[3],
                 "ffffff-000000|f8f8f8-000000", 1.0)
    print(ret)
    return ret
