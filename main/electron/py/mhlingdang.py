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


def 铃铛(deviceId):
    print('F_领取铃铛任务')
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    F_铃铛任务(window)


def F_铃铛任务(window):
    window.F_移动到游戏区域坐标(173, 335)
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    pyautogui.hotkey('alt', 'q')
    time.sleep(1)
    任务 = window.F_识别自定义任务()
    if('虫' in 任务 and '使用' in 任务):
        pyautogui.hotkey('alt', 'q')
        放虫(window, 任务)
    if('虫' in 任务 and '发现' in 任务):
        pyautogui.hotkey('alt', 'q')
        杀虫(window, 任务)
    if('找' in 任务 and '迷幻妖' in 任务):
        找迷幻妖(window, 任务)
    if('巧' in 任务):
        找巧智(window, 任务)
    if('使用' in 任务 and '招魂' in 任务):
        pyautogui.hotkey('alt', 'q')
        使用招魂(window, 任务)
    if('梦' in 任务):
        找梦魔(window, 任务)


def 找梦魔(window, 任务):
    point = window.findImgInWindow('all-ld-mym.png', area=(346, 84, 211, 105))
    if point != None:
        window.pointMove(point[0] + 10, point[1] + 5, 手指操作模式=True)
        time.sleep(1)
        任务 = window.F_识别自定义任务()
        ret = window.F_获取任务位置和坐标(任务)
        pyautogui.hotkey('alt', 'q')
        window.F_任务导航器(ret[0], ret[1])
        window.F_小地图寻路器(ret[1], None)
        pyautogui.press('f9')
        time.sleep(0.5)
        window.F_点击战斗()
        time.sleep(0.5)
        window.F_移动到游戏区域坐标(275, 340)
        utils.click()
        time.sleep(0.5)
        window.F_自动战斗2()
        utils.click()


def 使用招魂(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_任务导航器(ret[0], ret[1])
    window.F_小地图寻路器(ret[1], True)
    pyautogui.press('f9')
    pyautogui.hotkey('alt', 'e')
    for i in range(3):
        point = window.findImgInWindow(
            'all_ld_zht.png', area=(23, 270, 274, 230))
        if point != None:
            window.pointMove(point[0], point[1])
            utils.rightClick()
            pyautogui.hotkey('alt', 'e')
            window.focusWindow()
            utils.click()
            break
    time.sleep(5)
    window.F_点击战斗()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(275, 338)
    utils.click()
    time.sleep(0.5)
    window.F_自动战斗2()


def 找巧智(window, 任务):
    point = window.findImgInWindow('all-ld-qzm.png', area=(346, 84, 211, 105))
    if point != None:
        window.pointMove(point[0] + 10, point[1] + 5, 手指操作模式=True)
        time.sleep(1)
        任务 = window.F_识别自定义任务()
        ret = window.F_获取任务位置和坐标(任务)
        pyautogui.hotkey('alt', 'q')
        window.F_任务导航器(ret[0], ret[1])
        window.F_小地图寻路器(ret[1], None)
        pyautogui.press('f9')
        time.sleep(0.5)
        window.F_点击战斗()
        time.sleep(0.5)
        window.F_移动到游戏区域坐标(275, 338)
        utils.click()
        time.sleep(0.5)
        window.F_自动战斗2()
        utils.click()


def 找迷幻妖(window, 任务):
    point = window.findImgInWindow('all-ld-mhy.png', area=(346, 84, 211, 105))
    if point != None:
        window.pointMove(point[0] + 10, point[1] + 5, 手指操作模式=True)
        time.sleep(1)
        任务 = window.F_识别自定义任务()
        ret = window.F_获取任务位置和坐标(任务)
        pyautogui.hotkey('alt', 'q')
        window.F_任务导航器(ret[0], ret[1])
        window.F_小地图寻路器(ret[1], None)
        pyautogui.press('f9')
        time.sleep(0.5)
        window.F_点击战斗(True)
        time.sleep(0.5)
        window.F_移动到游戏区域坐标(275, 340)
        utils.click()
        time.sleep(0.5)
        window.F_自动战斗2()
        utils.click()


def 杀虫(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_任务导航器(ret[0], ret[1])
    window.F_小地图寻路器(ret[1], None)
    pyautogui.press('f9')
    time.sleep(0.5)
    window.F_点击战斗()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(275, 340)
    utils.click()
    time.sleep(0.5)
    window.F_自动战斗2()
    utils.click()


def 放虫(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_任务导航器(ret[0], ret[1])
    window.F_小地图寻路器(ret[1], True)
    pyautogui.press('f9')
    pyautogui.hotkey('alt', 'e')
    for i in range(3):
        point = window.findImgInWindow(
            'all-chong.png', area=(23, 270, 274, 230))
        if point != None:
            window.pointMove(point[0], point[1])
            utils.rightClick()
            pyautogui.hotkey('alt', 'e')
            window.focusWindow()
            utils.click()
            return


if __name__ == '__main__':
    print('F_领取铃铛任务')
    铃铛('9')
