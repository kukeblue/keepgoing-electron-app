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
        pyautogui.press('f2')
        time.sleep(2)
        for x in range(5):
            ret = baiduApi.F_大漠红色文字位置识别([window.windowArea[0], window.windowArea[1],
                                        window.windowArea[0] + 600, window.windowArea[1] + 800])
            print(ret)
            if(ret != None):
                window.pointMove(ret[0], ret[1])
                pyautogui.click()
                window.F_移动到游戏区域坐标(331, 549)
                pyautogui.click()
            pyautogui.keyDown('ctrl')
            pyautogui.press('tab')
            pyautogui.keyUp('ctrl')
            time.sleep(1)
        time.sleep(360)


if __name__ == '__main__':
    fire.Fire({
        'start': F_碗子山守护者,
    })
