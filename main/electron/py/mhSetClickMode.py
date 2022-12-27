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
import logUtil


def setOption(mode):
    mode = int(mode)
    pyHome = __file__.strip('mhSetClickMode.pyc')
    pyImageDir = pyHome + 'config\images'
    if(pyImageDir[0] == ":"):
        pyImageDir = "C" + pyImageDir
    logUtil.chLog(pyImageDir)
    with open(pyImageDir + '\\temp\\915.txt', "w", encoding='utf-8') as f:
        logUtil.chLog('设置驱动成功')
        f.write(str(mode))
        f.close()
            # utils.tcp_client_1.connect(("127.0.0.1", 61234))
    

if __name__ == '__main__':
    fire.Fire({
        'start': setOption,
    })
