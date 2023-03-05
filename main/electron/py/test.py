# 导入socket模块
import socket
from ctypes import *
import time
import os
import easyocr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
reader = easyocr.Reader(['ch_sim', 'en'])


def cnocr文字识别(path):
    res = reader.readtext(path)
    if(len(res) == 0):
        return ""
    print(res)
    return res[0][1]


cnocr文字识别('./1.png')