# coding=utf-8
import random
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


F_女娲神迹巡逻()
# if __name__ == '__main__':
#     fire.Fire({
#         'start': F_碗子山守护者,
#     })
