# coding=utf-8
import baiduApi

import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
import utils
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 卖装备(deviceId):
    print('F_领取丢垃圾')
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    window.F_卖装备(15)


if __name__ == '__main__':
    fire.Fire({
        'start': 卖装备,
    })
