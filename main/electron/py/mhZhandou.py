# coding=utf-8
from typing_extensions import Self
import mhWindow
import sys
import io
import time
import fire
import pyautogui
import utils
import random
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 无人值守模式():
    time.sleep(2)
    deviceId = '9'
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    pyautogui.click()
    while True:
        time.sleep(1)
        if(window.findImgInWindow("all-woyaoxiuxi.png", 0.9, area=(151, 381, 81, 35)) != None):
            print("我要休息")
            window.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            window.F_移动到游戏区域坐标(337, 551)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
            window.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            window.F_移动到游戏区域坐标(337, 551)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
            window.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            window.F_移动到游戏区域坐标(337, 551)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            window.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            window.F_移动到游戏区域坐标(337, 551)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(2)

def 飞机队四人模式挂机():
    print('启动队四人模式挂机')
    time.sleep(3)
    deviceId = '9'
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    回合数 = 0
    while True:
        time.sleep(0.5)
        if window.F_是否在战斗():
            print('进入战斗')
            while True:
                time.sleep(0.5)
                if window.F_是否战斗操作():
                    if(回合数 == 0):
                        飞机队操作(window)
                        回合数 = 回合数 + 1
                    else:
                        QQ操作(window)
                        回合数 = 回合数 + 1

                if window.F_是否结束战斗():
                    集体吃药(window)
                    回合数 = 0
                    break


def 集体吃药(window):
    window.F_吃药()
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    window.F_吃药()
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'tab')


def QQ操作(window):
    # 第一个号
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(1)
    # 第二个号
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    # 第三个号
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)


def 自动喊话模式(num):
    time.sleep(1)
    while True:
        for x in range(int(num)):
            pyautogui.press('up')
            time.sleep(1)
            pyautogui.press('enter')
            if(num > 1):
                pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
        randint_data = random.randint(3, 10)
        time.sleep(randint_data)


def 飞机队操作(window):
    # 第一个号
    window.F_移动到游戏区域坐标(320, 230, True)
    pyautogui.press('f3')
    utils.click()
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    # 第二个号
    window.F_移动到游戏区域坐标(320, 230, True)
    pyautogui.press('f3')
    utils.click()
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    # 第三个号
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)


无人值守模式()
# if __name__ == '__main__':
#     fire.Fire({
#         'lbc': 飞机队四人模式挂机,
#         'hh': 自动喊话模式,
#     })
# 自动喊话模式('4')
# 飞机队四人模式挂机('9')dfv
