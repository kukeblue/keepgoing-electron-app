# coding=utf-8
from tkinter import NO
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
import pydirectinput
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 抓鬼(deviceId):
    print('F_领取抓鬼任务')
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    pydirectinput.click()
    while True:
        F_领取抓鬼任务(window)


def F_领取抓鬼任务(window):
    window.F_导航到地府()
    F_领取钟馗任务(window)
    任务 = window.F_识别当前任务()
    ret = window.F_获取任务位置和坐标(任务)
    print(ret[0])
    window.F_任务导航器(ret[0], ret[1])
    if(ret[0] == '大唐境外'):
        window.F_小地图寻路器(ret[1], True)
    else:
        window.F_小地图寻路器(ret[1], None)
    pyautogui.press('f9')
    window.F_点击战斗()
    window.F_自动战斗2()
    pydirectinput.click()


def F_领取钟馗任务(window):
    window.F_小地图寻路器([38, 59], None)
    pyautogui.press('f9')
    # 点击钟馗
    window.F_移动到游戏区域坐标(522, 332)
    pydirectinput.doubleClick()
    time.sleep(1)
    # 好的我帮你
    if window.F_红色文字位置点击('我帮你'):
        # window.F_移动到游戏区域坐标(211, 340)
        #   pydirectinput.click()
        time.sleep(1)
        pydirectinput.click()
        F_使用天眼(window)
        time.sleep(1)
    else:
        F_领取钟馗任务(window)


def F_使用天眼(window):
    window.F_选中道具格子(15)
    time.sleep(0.2)
    pydirectinput.click(button="right")
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'e')


# if __name__ == '__main__':
#     fire.Fire({
#         'zg': 抓鬼,
#     })

if __name__ == '__main__':
    print('F_领取抓鬼任务')
    time.sleep(3)
    deviceId = str(9)
    抓鬼(deviceId)
