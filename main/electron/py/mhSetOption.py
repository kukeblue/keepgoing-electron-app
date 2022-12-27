# coding=utf-8
from typing_extensions import Self
import mhWindow
import sys
import io
import time
import fire
import pyautogui
import utils
import random


def setOption(userId):
    pyHome = __file__.strip('mhSetOption.pyc')
    pyImageDir = pyHome + 'config\images'
    if(pyImageDir[0] == ":"):
        pyImageDir = "C" + pyImageDir
    print(pyImageDir)
    with open(pyImageDir + '\\temp\\914.txt', "w", encoding='utf-8') as f:
            f.write(str(userId))
            f.close()

if __name__ == '__main__':
    fire.Fire({
        'start': setOption,
    })
