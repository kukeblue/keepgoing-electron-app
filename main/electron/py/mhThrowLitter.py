# coding=utf-8
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


def 丢垃圾():
    print('F_领取丢垃圾')
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.focusWindow()
    utils.click()
    window.F_丢垃圾(15)


if __name__ == '__main__':
    fire.Fire({
        'start': 丢垃圾,
    })
