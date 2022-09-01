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
from tkinter import messagebox
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def F_女娲神迹巡逻(window):
    logUtil.chLog('女娲神迹巡逻')
    points = [[250, 210], [527, 294], [221, 308], [
        451, 412], [396, 332], [471, 269], [303, 445]]
    lastPoint = None
    time.sleep(1)

    while True:
        index = random.randrange(0, 7, 1)
        point = points[index]
        if(lastPoint == point):
            continue
        pyautogui.press('tab')
        window.F_移动到游戏区域坐标(point[0], point[1], True)
        utils.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        window.F_是否结束寻路()
        window.F_自动战斗抓律法()
        res = F_检查女娲技能(window)
        if(res == True):
            # messagebox.showinfo('提示', res)
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
    return ret


def F_商店单间数量(window):
    携带数量 = [window.windowArea[0] + 338, window.windowArea[1] + 140, 60, 33]
    path = window.F_窗口区域截图('temp_orc_info.png', 携带数量)
    ret = baiduApi.cnocr文字识别(path)
    print(ret)
    return ret


def F_改名字(window):
    五行位置 = [window.windowArea[0] + 505, window.windowArea[1] + 357, 20, 20]
    path = window.F_窗口区域截图('temp_orc_info.png', 五行位置)
    ret = baiduApi.cnocr文字识别2(path)
    print('五行:' + ret)
    技能数 = '0'
    point = window.findImgInWindow(
        'all-empty-jn.png', 0.70, area=(480, 385, 43, 35))
    if(point == None):
        技能数 = '3'
    else:
        point = window.findImgInWindow(
            'all-empty-jn.png', 0.70, area=(440, 381, 43, 43))
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
    pyperclip.copy("律法女娲" + 名字)
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


# def F_集体改名():
#     MHWindow = mhWindow.MHWindow
#     window = MHWindow(1)
#     window.findMhWindow()
#     pyautogui.hotkey('alt', 'o')
#     time.sleep(2)
#     points = window.findImgsInWindow('all-lv-tou.png')
#     print(points)
#     for point in points:
#         window.pointMove(point[0] + 20, point[1] + 20)
#         utils.click()
#         pyautogui.press('tab')
#         window.F_移动到游戏区域坐标(220, 278)
#         time.sleep(1)
#         pyautogui.press('tab')
#         time.sleep(1)
#         utils.click()
#         utils.click()
#         utils.click()
#         time.sleep(1)
#         window.F_移动到游戏区域坐标(340, 290)
#     pyautogui.hotkey('alt', 'o')

def F_回商会(window):
    window.F_使用长安城飞行棋('红色长安城导标旗坐标_商会')
    pyautogui.press('f9')
    window.F_移动到游戏区域坐标(301, 222)
    utils.click()
    window.F_移动到游戏区域坐标(260, 378)
    utils.click()
    window.F_移动到游戏区域坐标(221, 341)
    utils.click()


def F_丢灵符(window):
    time.sleep(0.5)
    灵符女娲 = window.findImgInWindow(
        'all-lf-tou.png', 0.75, area=(14, 70, 193, 235))
    if(灵符女娲 != None):
        window.pointMove(灵符女娲[0] + 50, 灵符女娲[1] + 10)
        utils.click()
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


def F_检查女娲技能(window):
    time.sleep(1)
    pyautogui.hotkey('alt', 'o')
    time.sleep(1)
    携带数量 = F_获取携带数量(window)
    print(携带数量)
    if(携带数量 == '8/8' or 携带数量 == '818'):
        print('满了召唤兽')
        是否第一次查看技能 = True
        while True:
            window.F_移动到游戏区域坐标(184, 101)
            utils.click()
            F_丢灵符(window)
            识别名字 = window.findImgInWindow(
                'all-lyvw-1.png', 0.9, area=(14, 70, 193, 235))
            if(识别名字 == None):
                识别名字 = window.findImgInWindow(
                    'all-lyvw-2.png', 0.9, area=(14, 70, 193, 235))
            if(识别名字 == None):
                window.F_移动到游戏区域坐标(184, 196)
                utils.click()
                F_丢灵符(window)
                识别名字 = window.findImgInWindow(
                    'all-lyvw-1.png', 0.9, area=(14, 70, 193, 235))
                if(识别名字 == None):
                    识别名字 = window.findImgInWindow(
                        'all-lyvw-2.png', 0.9, area=(14, 70, 193, 235))
                if(识别名字 == None):
                    window.F_移动到游戏区域坐标(184, 272)
                    utils.click()
                    F_丢灵符(window)
                    携带数量 = F_获取携带数量(window)
                    识别名字 = window.findImgInWindow(
                        'all-lyvw-1.png', 0.9, area=(14, 70, 193, 235))
                    if(识别名字 == None):
                        识别名字 = window.findImgInWindow(
                            'all-lyvw-2.png', 0.9, area=(14, 70, 193, 235))
                    if(识别名字 == None):
                        print('携带数量')
                        print(携带数量)
                        pyautogui.hotkey('alt', 'o')
                        if((携带数量 == '6/8') or (携带数量 == '618') or (携带数量 == '7/8') or (携带数量 == '718') or (携带数量 == '7I8') or (携带数量 == '8/8') or (携带数量 == '818')):
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
        pyautogui.hotkey('alt', 'o')
        utils.rightClick()
        print('继续抓')


def F_去女娲(window):
    window.F_吃香2()
    window.F_导航到女娲神迹()
    window.F_吃动名草()


def F_补店():
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    # F_去女娲(window)
    # F_女娲神迹巡逻(window)
    # F_回商会(window)
    F_放入商店(window)


def F_放入商店(window):
    while True:
        num = F_商店单间数量(window)
        print(num)
        if(num == '16/16'):
            window.F_移动到游戏区域坐标(281, 491)
            utils.click()
            time.sleep(2)
            continue
        window.F_移动到游戏区域坐标(632, 463)
        utils.click()
        window.F_移动到游戏区域坐标(484, 492)
        utils.click()
        time.sleep(1)
        point = window.findImgInWindow(
            'all-shandian-lf.png', 0.70, area=(420, 240, 267, 226))
        if(point == None):
            messagebox.showinfo('提示', '没有宝宝了继续抓')
            F_商店扫描(window)
            break
        else:
            window.F_移动到游戏区域坐标(478, 491)
            utils.click()
            time.sleep(1)
            F_商店扫描(window)


def F_商店扫描(window):
    # window.F_移动到游戏区域坐标(337, 418)
    # utils.click()
    pyautogui.press('tab')
    window.F_移动到游戏区域坐标(222, 418)
    pyautogui.press('tab')
    utils.click()
    for x in range(10):
        pyautogui.press('left')
        time.sleep(0.1)
        pyautogui.press('delete')
    pyperclip.copy("25555")
    pyautogui.hotkey('ctrl', 'v')
    while True:
        window.F_移动到游戏区域坐标(374, 198)
        utils.click()
        上部改名 = F_循环上架(window)
        window.F_移动到游戏区域坐标(374, 390)
        utils.click()
        下部改名 = F_循环上架(window)
        if(上部改名 and 下部改名):
            break


def F_循环上架(window):
    point = window.findImgInWindow(
        'all-gaiming-lf.png', 0.90, area=(126, 189, 151, 210))
    if(point == None):
        print('未找到需要上架的货物')
        return True
    else:
        window.pointMove(point[0] + 10, point[1] + 5)
        utils.click()
        print('需要上架')

        window.F_移动到游戏区域坐标(354, 317)
        window.F_移动到游戏区域坐标(294, 417)
        utils.click()
        time.sleep(1)
        return False


F_补店()

# if __name__ == '__main__':
#     fire.Fire({
#         'lf': F_女娲神迹巡逻,
#     })
#
