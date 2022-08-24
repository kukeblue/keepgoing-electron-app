# coding=utf-8
from ast import Num
import random
from tkinter.tix import Tree
import baiduApi

import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import utils
import pyperclip
import pyautogui
import utils
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def F_女娲神迹巡逻():
    points = [[250, 210], [527, 294], [221, 308], [
        451, 412], [396, 332], [471, 269], [303, 445]]
    lastPoint = None
    time.sleep(1)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()

    while True:
        index = random.randrange(0, 7, 1)
        point = points[index]
        if(lastPoint == point):
            break
        pyautogui.press('tab')
        window.F_移动到游戏区域坐标(point[0], point[1], True)
        utils.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        window.F_是否结束寻路()
        window.F_自动战斗抓律法()
        res = F_检查女娲技能(window)
        if(res):
            break


def F_获取方式数字(window):
    丢弃数字位置 = [window.windowArea[0] + 300, window.windowArea[1] + 267, 48, 30]
    path = window.F_窗口区域截图('temp_orc_info.png', 丢弃数字位置)
    ret = baiduApi.cnocr文字识别(path)
    print(ret)
    num = "".join(list(filter(str.isdigit, ret)))
    return num


def F_获取携带数量(window):
    携带数量 = [window.windowArea[0] + 128, window.windowArea[1] + 282, 30, 33]
    path = window.F_窗口区域截图('temp_orc_info.png', 携带数量)
    ret = baiduApi.cnocr文字识别(path)
    print(ret)
    num = "".join(list(filter(str.isdigit, ret)))
    return num


def F_改名字(window):
    五行位置 = [window.windowArea[0] + 505, window.windowArea[1] + 357, 20, 20]
    path = window.F_窗口区域截图('temp_orc_info.png', 五行位置)
    ret = baiduApi.cnocr文字识别2(path)
    print('五行:' + ret)
    技能数 = '0'
    point = window.findImgInWindow(
        'all-empty-jn.png', 0.75, area=(480, 385, 43, 35))
    if(point == None):
        技能数 = '3'
    else:
        point = window.findImgInWindow(
            'all-empty-jn.png', 0.75, area=(440, 381, 43, 43))
        if(point == None):
            技能数 = '2'
        else:
            技能数 = '1'
    名字 = ret + 技能数
    pyautogui.press('tab')
    window.F_移动到游戏区域坐标(282, 293)
    pyautogui.press('tab')
    utils.click()
    for x in range(10):
        pyautogui.press('left')
        time.sleep(0.1)
        pyautogui.press('delete')
    pyperclip.copy(名字)
    pyautogui.hotkey('ctrl', 'v')
    window.F_移动到游戏区域坐标(340, 290)
    utils.click()
    time.sleep(1)

    # window.F_移动到游戏区域坐标(266, 306)
    # pyautogui.press('tab')
    # utils.click()
    # time.sleep(2)
    # pyautogui.write(ret1)
    # print(ret1)
    # return


def F_检查女娲技能(window):
    time.sleep(1)
    pyautogui.hotkey('alt', 'o')
    time.sleep(1)
    携带数量 = F_获取携带数量(window)
    if(携带数量 == '8/8' or 携带数量 == '818'):
        print('满了召唤兽')
        是否第一次查看技能 = True
        while True:
            window.F_移动到游戏区域坐标(184, 101)
            utils.click()
            识别名字 = window.findImgInWindow(
                'all-lyvw-1.png', 0.9, area=(14, 70, 193, 235))
            if(识别名字 == None):
                识别名字 = window.findImgInWindow(
                    'all-lyvw-2.png', 0.9, area=(14, 70, 193, 235))
            if(识别名字 == None):
                window.F_移动到游戏区域坐标(184, 273)
                utils.click()
                识别名字 = window.findImgInWindow(
                    'all-lyvw-1.png', 0.9, area=(14, 70, 193, 235))
                if(识别名字 == None):
                    识别名字 = window.findImgInWindow(
                        'all-lyvw-2.png', 0.9, area=(14, 70, 193, 235))
                if(识别名字 == None):
                    携带数量 = F_获取携带数量(window)
                    pyautogui.hotkey('alt', 'o')
                    if(携带数量 == '6/8' or 携带数量 == '618' or 携带数量 == '7/8' or 携带数量 == '718' or 携带数量 == '8/8' or 携带数量 == '818'):
                        return True
                    else:
                        return False
            window.pointMove(识别名字[0], 识别名字[1])
            if(是否第一次查看技能):
                utils.rightClick()
                是否第一次查看技能 = False
            else:
                utils.click()
            time.sleep(1.5)
            技能善恶 = window.findImgInWindow('all-jn-se.png')
            if(技能善恶 == None):
                window.F_移动到游戏区域坐标(180, 472)
                utils.click()
                window.F_移动到游戏区域坐标(328, 342)
                utils.click()
                time.sleep(1)
                num = F_获取方式数字(window)
                pyautogui.press('tab')
                window.F_移动到游戏区域坐标(267, 306)
                pyautogui.press('tab')
                utils.click()
                pyautogui.write(num)
                time.sleep(0.5)
                window.F_移动到游戏区域坐标(517, 338)
                utils.click()
                time.sleep(0.5)
                window.focusWindow()
                time.sleep(0.5)
            else:
                F_改名字(window)
        time.sleep(1)
    else:
        print('继续抓')
        pyautogui.hotkey('alt', 'o')


F_女娲神迹巡逻()
# MHWindow = mhWindow.MHWindow
# window = MHWindow(1)
# window.findMhWindow()
# F_改名字(window)
