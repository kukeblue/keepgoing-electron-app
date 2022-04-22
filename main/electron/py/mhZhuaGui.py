# coding=utf-8
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


def F_领取抓鬼任务():
    print(F_领取抓鬼任务)


if __name__ == '__main__':
    fire.Fire({
        'zhuaGui': F_领取抓鬼任务,
    })
