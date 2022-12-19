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
import ddServer


def setOption(mode):
    mode = int(mode)
    if(mode == 2):
        utils.tcp_client_1.connect(("127.0.0.1", 61234))
    utils.mode = mode

if __name__ == '__main__':
    fire.Fire({
        'start': setOption,
    })
