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
        F_检查女娲技能()


def F_获取方式数字(window):
    丢弃数字位置 = [window.windowArea[0] + 300, window.windowArea[1] + 267, 48, 30]
    path = window.F_窗口区域截图('temp_orc_info.png', 丢弃数字位置)
    ret = baiduApi.cnocr文字识别(path)
    print(ret)
    num = "".join(list(filter(str.isdigit, ret)))
    return num


def F_改名字(window):
    五行位置 = [window.windowArea[0] + 498, window.windowArea[1] + 353, 30, 30]
    path = window.F_窗口区域截图('temp_orc_info.png', 五行位置)
    ret = baiduApi.cnocr文字识别(path)
    print('五行:' + ret)
    技能数 = '0'
    # point = window.findImgInWindow(
    #     'all-empty-jn.png', 0.75, area=(523, 383, 43, 45))
    # if(point == None):
    #     point = window.findImgInWindow(
    #         'all-empty-jn.png', 0.75, area=(479, 383, 43, 45))
    # else:
    #     技能数 = '4'
    # if(point == None):
    #     point = window.findImgInWindow(
    #         'all-empty-jn.png', 0.75, area=(436, 383, 43, 45))
    # else:
    #     技能数 = '3'
    # if(point == None):
    #     技能数 = '1'
    # else:
    #     技能数 = '2'
    point = window.findImgInWindow(
        'all-empty-jn.png', 0.75, area=(479, 383, 43, 45))
    if(point != None):
        技能数 = '3'
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


def F_检查女娲技能():
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    time.sleep(1)
    pyautogui.hotkey('alt', 'o')
    time.sleep(1)
    point = window.findImgInWindow('all-8-1-8.png',  0.95)
    if(point != None):
        print('满了召唤兽')
        是否第一次查看技能 = True
        while True:
            识别名字 = window.findImgInWindow('all-lyvw-1.png')
            if(识别名字 == None):
                识别名字 = window.findImgInWindow('all-lyvw-2.png')
            if(识别名字 == None):
                break
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


MHWindow = mhWindow.MHWindow
window = MHWindow(1)
window.findMhWindow()
F_改名字(window)
# if __name__ == '__main__':
#     fire.Fire({
#         'start': F_碗子山守护者,
#     })
