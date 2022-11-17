# from paddleocr import PaddleOCR
import socket
import win32gui as w
from pickle import TRUE
import time
import baiduApi
import win32gui
import win32api
import win32con
import pyautogui
import mouse
import re
from win32com.client import Dispatch
op = Dispatch("op.opsoft")
handle = 0


tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2 通过客户端套接字的connect方法与服务器套接字建立连接
# 参数介绍：前面的ip地址代表服务器的ip地址，后面的61234代表服务端的端口号 。
tcp_client_1.connect(("127.0.0.1", 61234))
# while True:
#     time.sleep(1)
#     send_data = "rigthClick".encode(encoding='utf-8')
#     tcp_client_1.send(send_data)
#     recv_data = tcp_client_1.recv(1024)
#     print(recv_data.decode(encoding='utf-8'))


def bindOp():
    real = pyautogui.position()
    global handle
    handle = win32gui.WindowFromPoint((real[0], real[1]))
    title = w.GetWindowText(handle)
    print(title)
    res = re.findall(r'[\[](.*?)[]]', title)[1]
    # op.BindWindow(handle, "normal", "windows", "windows", 1)
    win32gui.SetForegroundWindow(handle)
    print('当前角色ID为: ' + res)
    return [res, handle]


def click():
    send_data = "click".encode(encoding='utf-8')
    tcp_client_1.send(send_data)
    recv_data = tcp_client_1.recv(1024)
    print(recv_data.decode(encoding='utf-8'))


def move(x, y):
    if((abs(x) + abs(y)) < 100):
        mouse.move(x, y, absolute=False, duration=0.05)
    else:
        mouse.move(x, y, absolute=False, duration=0.05)


def doubleClick():
    send_data = "doubleClick".encode(encoding='utf-8')
    tcp_client_1.send(send_data)
    recv_data = tcp_client_1.recv(1024)
    print(recv_data.decode(encoding='utf-8'))


def rightClick():
    send_data = "rightClick".encode(encoding='utf-8')
    tcp_client_1.send(send_data)
    recv_data = tcp_client_1.recv(1024)
    print(recv_data.decode(encoding='utf-8'))
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
