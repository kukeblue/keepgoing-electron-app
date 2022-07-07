# coding=utf-8
import mhWindow
import sys
import io
import time
import fire
import pyautogui
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 飞机队四人模式挂机(deviceId):
    print('启动队四人模式挂机')
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    pyautogui.click()
    回合数 = 0
    while True: 
        time.sleep(0.5)
        if window.F_是否在战斗():
            print('进入战斗')
            while True:
                time.sleep(0.5)
                if window.F_是否战斗操作():
                    if( 回合数 == 0):
                        飞机队操作(window)
                        回合数 = 回合数 + 1
                    else:
                        QQ操作(window)
                        回合数 = 回合数 + 1

                if window.F_是否结束战斗():
                    回合数 = 0
                    break

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

def 飞机队操作(window):
    # 第一个号
    window.F_移动到游戏区域坐标(320, 230, True)
    pyautogui.press('f3')
    pyautogui.click()
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(0.3)
    # 第二个号
    window.F_移动到游戏区域坐标(320, 230, True)
    pyautogui.press('f3')
    pyautogui.click()
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


if __name__ == '__main__':
    # fire.Fire({
    #     'lbc': 飞机队四人模式挂机,
    # })
    飞机队四人模式挂机('9')
