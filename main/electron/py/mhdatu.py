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
import utils
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 到店小二领取任务(window):

    ret = baiduApi.op.FindMultiColor(
        window.windowArea2[0] + 641, window.windowArea2[1] + 135, window.windowArea2[0] + 680, window.windowArea2[3] + 175, '00ff00', '11|2|00ff00', 0.8, 0)
    if(ret[1] > 0):
        print('有任务')
    else:
        window.F_使用长安城飞行棋('红色长安城导标旗坐标_酒店')
        time.sleep(1)
        pyautogui.press('f9')
        window.F_移动到游戏区域坐标(533, 165)
        utils.click()
        time.sleep(3)
        window.F_移动到游戏区域坐标(559, 284)
        utils.click()
        time.sleep(3)
        pyautogui.press('f9')
    while True:
        ret = baiduApi.op.FindMultiColor(
            window.windowArea2[0] + 641, window.windowArea2[1] + 135, window.windowArea2[0] + 680, window.windowArea2[3] + 175, '00ff00', '11|2|00ff00', 0.8, 0)
        if(ret[1] > 0):
            任务 = 读取任务(window)
            ret = window.F_获取任务位置和坐标(任务)
            window.F_任务导航器(ret[0], ret[1])
            window.F_小地图寻路器(ret[1], None)
            pyautogui.press('f9')
            window.F_点击战斗(右键点击=True)
            window.F_移动到游戏区域坐标(209, 339)
            utils.click()
            window.F_自动战斗2()
            utils.click()
            break
        else:
            到店小二附近(window)
            pyautogui.press('f9')
            window.findMhWindow()
            点击店小二(window)
            time.sleep(1)


def 到店小二附近(window):
    while True:
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-1.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 60, point[1])
            utils.click()
            time.sleep(3)
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-2.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 60, point[1])
            utils.click()
            time.sleep(3)
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-3.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 60, point[1])
            utils.click()
            time.sleep(3)
            window.focusWindow()
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-4.png', confidence=0.8)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 60, point[1])
            utils.click()
            time.sleep(3)
            window.focusWindow()
            break


def 点击店小二(window):
    for x in range(3):
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-1.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 5, point[1])
            utils.click()
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-2.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 5, point[1])
            utils.click()
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-3.png', confidence=0.6)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 5, point[1])
            utils.click()
            break
        point = window.findImgInWindowReturnWindowPoint(
            'all-xiaoer-4.png', confidence=0.8)
        if(point):
            window.F_移动到游戏区域坐标(point[0] + 60, point[1])
            utils.click()
            break
    time.sleep(0.6)
    point = window.findImgInWindow(
        'all-xiaoer-duihua.png', area=(151, 343, 103, 36))
    if(point):
        window.F_移动到游戏区域坐标(189, 354)
        utils.click()
        time.sleep(1)
        utils.click()


def 读取任务(window):
    time.sleep(0.6)
    任务 = window.F_识别当前任务()
    print(任务)
    return 任务


deviceId = '9'
print('到店小二领取任务')
time.sleep(3)
deviceId = str(deviceId)
MHWindow = mhWindow.MHWindow
window = MHWindow(1, deviceId)
window.findMhWindow()
window.focusWindow()
while True:
    到店小二领取任务(window)
