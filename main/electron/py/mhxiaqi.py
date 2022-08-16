# coding=utf-8
from tkinter import N, NO
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


def 下棋():
    print('F_领取下棋任务')
    time.sleep(2)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    # 使用盒子(window)

    执行任务(window)


def 执行任务(window):
    pyautogui.hotkey('alt', 'q')
    time.sleep(1)
    任务 = window.F_识别自定义任务()
    ret = window.F_获取任务位置和坐标(任务)
    print(ret[0])
    window.F_任务导航器(ret[0], ret[1])
    ret = baiduApi.op.FindMultiColor(window.windowArea[0] + 348, window.windowArea[1] + 85,
                                     window.windowArea[0] + 348 + 200, window.windowArea[1] + 85 + 99, 'ff0000', '9|0|ff0000,31|0|ff0000', 0.95, 0)
    if ret[0] > 0:
        logUtil.chLog(ret)
        window.pointMove(ret[1], ret[2], False, True)
        utils.click()
        time.sleep(0.5)
    pyautogui.hotkey('alt', 'q')
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(205, 340)
    utils.click()
    window.F_自动战斗2()


def 使用盒子(window):
    window.F_打开道具()
    time.sleep(1)
    point = window.findImgInWindow(
        'all-qipan.png')
    if point != None:
        window.pointMove(point[0], point[1])
        utils.rightClick()
        time.sleep(0.5)
        utils.rightClick()
        time.sleep(0.5)
        utils.rightClick()
        time.sleep(2)
        ret = baiduApi.op.FindMultiColor(window.windowArea[0] + 285, window.windowArea[1] + 111,
                                         window.windowArea[0] + 285 + 395, window.windowArea[1] + 111 + 395, 'efe1aa', '1|0|f5e5ae,0|1|f6e6b0,0|2|f3e3ac,2|0|f4e4ad', 0.80, 0)
        if ret[0] > 0:
            logUtil.chLog(ret)
            window.pointMove(ret[1], ret[2])
            utils.click()
    window.F_打开道具()
    time.sleep(1)
    point = window.findImgInWindow(
        'all-qipan.png')
    if point != None:
        window.pointMove(point[0], point[1])
        utils.rightClick()
    window.F_移动到游戏区域坐标(176, 355)
    utils.click()
    time.sleep(0.5)
    utils.click()
    window.F_关闭道具()


def F_领取抓鬼任务(window):
    while True:
        任务 = window.F_识别抓鬼任务()
        if(任务['鬼王'] != None):
            鬼王任务 = 任务['鬼王']
            ret = window.F_获取任务位置和坐标(鬼王任务)
            print(ret[0])
            window.F_任务导航器(ret[0], ret[1])
            if(ret[0] == '大唐境外'):
                window.F_小地图寻路器(ret[1], True)
            else:
                window.F_小地图寻路器(ret[1], None)
            pyautogui.press('f9')
            window.F_点击战斗()
            window.F_自动战斗2()
            window.F_移动到游戏区域坐标(665, 301)
            utils.click()
        if(任务['捉鬼'] != None):
            print(任务['捉鬼'])
            小鬼任务 = 任务['捉鬼']
            ret = window.F_获取任务位置和坐标(小鬼任务)
            print(ret[0])
            window.F_任务导航器(ret[0], ret[1])
            if(ret[0] == '大唐境外'):
                window.F_小地图寻路器(ret[1], True)
            else:
                window.F_小地图寻路器(ret[1], None)
            pyautogui.press('f9')
            window.F_点击战斗()
            window.F_自动战斗2()
        window.F_导航到地府()
        F_领取大鬼任务(window)
        F_领取钟馗任务(window)


def F_领取大鬼任务(window):
    window.F_小地图寻路器([104, 55], None)
    pyautogui.press('f9')
    window.F_移动到游戏区域坐标(447, 198)
    utils.click()
    time.sleep(1)
    pyautogui.press('f9')
    window.F_移动到游戏区域坐标(628, 337)
    utils.click()
    time.sleep(2)
    pyautogui.press('f9')
    window.F_移动到游戏区域坐标(371, 233)
    utils.click()
    window.F_移动到游戏区域坐标(273, 394)
    utils.click()
    time.sleep(1)
    utils.click()
    window.F_移动到游戏区域坐标(256, 502)
    utils.click()
    utils.click()
    time.sleep(3)


def F_领取钟馗任务(window):

    window.F_小地图寻路器([38, 59], None)
    pyautogui.press('f9')
    # 点击钟馗
    window.F_移动到游戏区域坐标(522, 332)
    utils.doubleClick()
    time.sleep(1)
    # 好的我帮你
    if window.F_红色文字位置点击('我帮你'):
        # window.F_移动到游戏区域坐标(211, 340)
        #   utils.click()
        time.sleep(1)
        utils.click()
        F_使用天眼(window)
        time.sleep(1)
    else:
        F_领取钟馗任务(window)


def F_使用天眼(window):
    window.F_选中道具格子(15)
    time.sleep(0.2)
    utils.rightClick()
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'e')


# if __name__ == '__main__':
#     fire.Fire({
#         'zg': 抓鬼,
#     })

if __name__ == '__main__':
    print('F_领取抓鬼任务')
    time.sleep(3)
    下棋()
