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
import pydirectinput
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def 连点器(deviceId):
    while True:
          pydirectinput.click()
        time.sleep(1)


if __name__ == '__main__':
    fire.Fire({
        'start': 连点器,
    })
