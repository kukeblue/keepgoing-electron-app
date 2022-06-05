# coding=utf-8
import baiduApi
from cv2 import log
import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def F_碗子山守护者(deviceId):
    time.sleep(1)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    while True:
        while True:
            time.sleep(1)
            if(window.F_是否在战斗() == False):
                pyautogui.press('f5')
                pyautogui.press('f5')
                window.F_移动到游戏区域坐标(331, 549)
                pyautogui.click()
                pyautogui.press('f2')
                window.F_移动到游戏区域坐标(269, 418)
                pyautogui.click()
                pyautogui.keyDown('ctrl')
                pyautogui.press('tab')
                pyautogui.keyUp('ctrl')
                time.sleep(1)
                for x in range(3):
                    # ret = baiduApi.F_大漠红色文字位置识别([window.windowArea[0], window.windowArea[1],
                    #                             window.windowArea[0] + 600, window.windowArea[1] + 800])
                    # print(ret)
                    # if(ret != None):
                    window.F_移动到游戏区域坐标(189, 399)
                    pyautogui.click()
                    window.F_移动到游戏区域坐标(331, 549)
                    pyautogui.click()
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('tab')
                    pyautogui.keyUp('ctrl')
                    time.sleep(1)
                break
        time.sleep(360)


if __name__ == '__main__':
    fire.Fire({
        'start': F_碗子山守护者,
    })
