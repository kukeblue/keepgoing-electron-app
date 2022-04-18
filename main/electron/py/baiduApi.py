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

op.SetDict(0, pyZhikuDir + '\\baotuzuobiao.txt')


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
    str = op.Ocr(area[0], area[1], area[2], area[3],
                 "00ff00-000000", 0.98)
    return str
