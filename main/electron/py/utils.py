# from paddleocr import PaddleOCR
from pickle import TRUE
import time
import baiduApi
from win32com.client import Dispatch
op = Dispatch("op.opsoft")
# ocr = PaddleOCR(use_angle_cls=True, use_gpu=True, show_log=False)


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
    writeText('ch.1993.com')
