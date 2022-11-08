# coding=utf-8
from telnetlib import theNULL
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
import networkApi
import utils
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 抓鬼(是否抓大鬼):
    print('F_领取抓鬼任务')
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    if(networkApi.doUpdateRoleStatus(window.gameId, '抓鬼')):
        F_领取抓鬼任务(window, 是否抓大鬼)


def F_领取抓鬼任务(window, 是否抓大鬼):
    logUtil.chLog('开始抓大鬼')
    logUtil.chLog(是否抓大鬼)
    抓鬼次数 = 0
    while True:
        if(是否抓大鬼 == 1):
            抓鬼次数 = 抓鬼次数 + 1
        else:
            抓鬼次数 = 抓鬼次数 + 0.5
        if(抓鬼次数 == 5):
            window.F_吃香2()
            window.F_集体酒肆()
            抓鬼次数 = 0
        任务 = window.F_识别抓鬼任务()
        if(是否抓大鬼 == 1 and 任务['鬼王'] != None):
            pyautogui.hotkey('alt', 'q')
            time.sleep(0.5)
            鬼王任务 = window.F_识别自定义任务()
            logUtil.chLog(鬼王任务)
            window.F_移动到游戏区域坐标(178, 341)
            utils.click()
            pyautogui.hotkey('alt', 'q')
            ret = window.F_获取任务位置和坐标(鬼王任务)
            print(ret[0])
            window.F_任务导航器(ret[0], ret[1])
            window.F_点击小地图出入口按钮()
            window.F_小地图寻路器(ret[1], True)
            if(ret[0] == '地狱迷宫'):
                time.sleep(20)
            pyautogui.press('f9')
            window.F_点击战斗()
            window.F_抓鬼自动战斗()
            window.F_点击小地图出入口按钮()
            # window.F_移动到游戏区域坐标(665, 301)
            # utils.click()
        if(任务['捉鬼'] != None):
            logUtil.chLog(任务['捉鬼'])
            小鬼任务 = 任务['捉鬼']
            ret = window.F_获取任务位置和坐标(小鬼任务)
            print(ret[0])
            time.sleep(2)
            window.F_任务导航器(ret[0], ret[1])
            window.F_点击小地图出入口按钮()
            window.F_小地图寻路器(ret[1], True)

            pyautogui.press('f9')
            window.F_点击战斗()
            window.F_抓鬼自动战斗()
            time.sleep(1)
            window.F_点击小地图出入口按钮()
            if(是否抓大鬼 == 1):
                pyautogui.hotkey('alt', 'q')
                window.F_移动到游戏区域坐标(178, 341)
                utils.click()
                pyautogui.hotkey('alt', 'q')
                window.focusWindow()
        window.F_导航到地府()
        if(是否抓大鬼 == 1):
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


if __name__ == '__main__':
    fire.Fire({
        'zg': 抓鬼,
    })

# if __name__ == '__main__':
#     print('F_领取抓鬼任务')
#     time.sleep(3)
#     MHWindow = mhWindow.MHWindow
#     window = MHWindow(1)
#     window.findMhWindow()
#     window.focusWindow()
#     抓鬼(window)
