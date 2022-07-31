# from paddleocr import PaddleOCR
import win32gui as w
from pickle import TRUE
import time
import baiduApi
import win32gui
import win32api
import win32con
import pyautogui
import re
from win32com.client import Dispatch
op = Dispatch("op.opsoft")
handle = 0


def bindOp():
    real = pyautogui.position()
    global handle
    handle = win32gui.WindowFromPoint((real[0], real[1]))
    title = w.GetWindowText(handle)
    print(title)
    res = re.findall(r'[[](.*?)[]]', title)[1]
    op.BindWindow(handle, "normal", "windows", "windows", 1)
    win32gui.SetForegroundWindow(handle)
    print('当前角色ID为: ' + res)
    return res


def click():
    global handle
    if(handle == 0):
        pyautogui.click()
    else:
        win32gui.SendMessage(handle, win32con.WM_ACTIVATE,
                             win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        time.sleep(0.2)


def doubleClick():
    global handle
    if(handle == 0):
        pyautogui.click()
        pyautogui.click()
    else:
        win32gui.SendMessage(handle, win32con.WM_ACTIVATE,
                             win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(
            handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        time.sleep(0.2)


def rightClick():
    global handle
    if(handle == 0):
        pyautogui.rightClick()
    else:
        win32gui.SendMessage(
            handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON)
        win32gui.SendMessage(
            handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON)
        time.sleep(0.2)


def getPointColor(x, y):
    return op.getColor(x, y)


def writeText(text):
    if text == 'ch.1993.com':
        writeText('ch')
        op.KeyPress('190')
        writeText('1993')
        op.KeyPress('190')
        writeText('com')
    else:
        for key in text:
            time.sleep(0.25)
            if key.isupper():
                op.KeyDown(16)
                time.sleep(0.1)
                op.KeyPressChar(key)
                op.KeyUp(16)
            else:
                op.KeyPressChar(key)


def pressKeyGroup(key1, key2):
    op.KeyDown(key1)
    time.sleep(0.1)
    op.KeyPress(key2)
    op.KeyUp(key1)


def F_本地文字识别(path):
    text = ocr.ocr(path, cls=True)
    ret = ''
    for t in text:
        ret = ret + t[1][0]
    return ret


def F_通用文字识别(path):
    try:
        baiduRetStr = baiduApi.getImageText(path)
        print(baiduRetStr['words_result'])
        str = ''
        for item in baiduRetStr['words_result']:
            str = str + item['words']
        print(str)
        return str
    except IOError:
        print(0)
        return 0


def getGameVerificationCode():
    try:
        hwnd = op.findWindow('', '乾坤辅助平台')
        ret = op.bindWindow(hwnd, "normal", "normal", "normal", 0)
        print(ret)
        op.Capture(140, 180, 350, 223, "screen.bmp")
        baiduRetStr = baiduApi.getImageText('screen.bmp')
        print(baiduRetStr['words_result'])
        verificationCode = ''
        for item in baiduRetStr['words_result']:
            verificationCode = verificationCode + item['words']
        print(verificationCode)
        return verificationCode
    except IOError:
        print(0)
        return 0


if __name__ == "__main__":
    time.sleep(3)
    bindOp()
    rightClick()
