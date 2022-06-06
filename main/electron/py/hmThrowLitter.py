# coding=utf-8
import baiduApi
from cv2 import log
import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 丢垃圾(deviceId):
    print('F_领取丢垃圾')
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    pyautogui.click()
    window.F_丢垃圾(15)

if __name__ == '__main__':
    fire.Fire({
        'start': 丢垃圾,
    })
