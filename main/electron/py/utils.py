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
import mouse
from win32com.client import Dispatch
op = Dispatch("op.opsoft")
handle = 0
import socket
mode = 1
pyHome = __file__.strip('utils.pyc')
pyZhikuDir2 = pyHome + 'config\images'

tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2 通过客户端套接字的connect方法与服务器套接字建立连接
# 参数介绍：前面的ip地址代表服务器的ip地址，后面的61234代表服务端的端口号 。
if(pyZhikuDir2[0] == ":"):
    pyZhikuDir2 = "C" + pyZhikuDir2

with open(pyZhikuDir2 + '/temp/915.txt', "r", encoding='utf-8') as f:
    mode = f.read()
    if(mode == "2"):
        tcp_client_1.connect(("127.0.0.1", 61234))
    f.close()

def bindOp():
    real = pyautogui.position()
    global handle
    handle = win32gui.WindowFromPoint((real[0], real[1]))
    title = w.GetWindowText(handle)
    print(title)
    res = re.findall(r'[[](.*?)[]]', title)[1]
    area = re.findall(r'[\[](.*?)[]]', title)[0]
    roleName=title[15: -1]
    roleName = roleName.split('-')[1].strip()
    op.BindWindow(handle, "normal", "windows", "windows", 1)
    win32gui.SetForegroundWindow(handle)
    print('当前角色ID为: ' + roleName)
    return [res, handle, area, roleName]



def click():
    if(mode == 2):
        send_data = "click".encode(encoding='utf-8')
        tcp_client_1.send(send_data)
        recv_data = tcp_client_1.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
    else:
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
    if(mode == 2):
        send_data = "doubleClick".encode(encoding='utf-8')
        tcp_client_1.send(send_data)
        recv_data = tcp_client_1.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
    else:
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
    if(mode == 2):
        send_data = "rightClick".encode(encoding='utf-8')
        tcp_client_1.send(send_data)
        recv_data = tcp_client_1.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
        time.sleep(0.2)
    else:
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

def move(x, y):
    if((abs(x) + abs(y)) < 100):
        mouse.move(x, y, absolute=False, duration=0.05)
    else:
        mouse.move(x, y, absolute=False, duration=0.1)


def getGameVerificationCode():
    try:
        hwnd = op.findWindow('', '摸金辅助')
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