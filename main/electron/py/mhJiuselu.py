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


def 九色鹿(window):
    print('F_领取抓鬼任务')
    time.sleep(2)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()


def 九色鹿皇宫七(window):
    window.任务栏点击(686,  165)
    time.sleep(2)
    window.F_是否结束寻路()
    关闭对话()
    window.任务栏点击(750,  175)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(390, 377)
    utils.click()
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(419, 158)
    utils.click()


def 九色鹿魔窟六(window):
    window.任务栏点击(658,  180)
    time.sleep(2)
    window.F_是否结束寻路()
    关闭对话(window)
    window.任务栏点击(695,  167)
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(195, 339)
    utils.click()
    time.sleep(2)
    window.任务栏点击(704,  166)
    time.sleep(1)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(277, 357)
    utils.click()
    window.F_自动战斗2()
    关闭对话(window)
    window.F_移动到游戏区域坐标(480, 270)
    utils.click()
    time.sleep(1)
    window.F_移动到游戏区域坐标(200, 340)
    utils.click()
    window.F_自动战斗2()
    关闭对话(window)
    window.F_移动到游戏区域坐标(400, 179)
    utils.click()
    关闭对话(window)
    window.F_移动到游戏区域坐标(705, 323)
    utils.click()
    time.sleep(1)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(403, 183)
    utils.click()
    关闭对话(window)


def 九色鹿调达五(window):
    window.任务栏点击(685,  165)
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(204, 361)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(1)
    window.任务栏点击(668,  165)
    time.sleep(10)
    window.F_移动到游戏区域坐标(204, 361)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    window.任务栏点击(675,  165)
    time.sleep(5)
    window.F_移动到游戏区域坐标(222, 339)
    utils.click()
    window.F_自动战斗2()
    关闭对话(window)


def 九色鹿灵芝娃娃四(window):
    window.F_移动到游戏区域坐标(705, 167, False, True)
    utils.click()
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(257, 340)
    window.F_自动战斗2()
    window.F_移动到游戏区域坐标(665, 300)
    utils.click()
    window.F_移动到游戏区域坐标(747, 165)
    utils.click()
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(286, 416)
    utils.click()
    关闭对话(window)
    window.任务栏点击(744,  167)
    time.sleep(2)
    window.F_是否结束寻路()
    window.F_移动到游戏区域坐标(237, 361)
    utils.click()
    time.sleep(60)
    关闭对话()


def 关闭对话(window):
    window.F_移动到游戏区域坐标(665, 300)
    utils.click()


def 九色鹿离开深林三(window):
    window.F_移动到游戏区域坐标(684, 167, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(667, 300)
    utils.click()
    window.F_移动到游戏区域坐标(703, 183, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(231, 337, False, True)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(708, 166, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(665, 298, False, True)
    utils.click()


def 九色鹿战斗二(window):
    # 给与布
    window.F_移动到游戏区域坐标(738, 167, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(429, 506)
    window.F_移动到游戏区域坐标(266, 417)
    utils.click()
    # 看看发生了什么
    window.F_移动到游戏区域坐标(688, 169, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(196, 360)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    # 动画
    time.sleep(10)
    # 河边
    window.F_移动到游戏区域坐标(664, 179, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(241, 357)
    utils.click()
    window.F_移动到游戏区域坐标(679, 167, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(184, 336)
    utils.click()
    window.F_自动战斗()
    window.F_移动到游戏区域坐标(664, 302)
    utils.click()


def 九色鹿入场战斗一(window):
    print('F_领取抓鬼任务')
    time.sleep(2)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.F_移动到游戏区域坐标(760, 169, False, True)
    utils.click()
    window.F_是否结束寻路()
    window.focusWindow()
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(219, 382)
    utils.click()
    window.F_移动到游戏区域坐标(680, 169, False, True)
    utils.click()
    window.F_移动到游戏区域坐标(317, 358)
    utils.click()
    time.sleep(0.5)
    utils.click()
    time.sleep(0.5)
    utils.click()
    window.F_自动战斗()
    window.F_移动到游戏区域坐标(667, 302)
    utils.click()


if __name__ == '__main__':
    print('F_领取抓鬼任务')
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.focusWindow()
    # 九色鹿入场战斗一(window)
    # 九色鹿战斗二(window)
    # 九色鹿离开深林三(window)
    # 九色鹿灵芝娃娃四(window)
    # 九色鹿调达五(window)
    九色鹿魔窟六(window)
    # 九色鹿皇宫七(window)
