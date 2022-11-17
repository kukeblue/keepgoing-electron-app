import os
import win32gui as w
import win32gui
import win32api
import time
import baiduApi
import random
import pyautogui
import mouse
import re
from ctypes import *
import atexit
if __name__ == '__main__':
    objdll = windll.LoadLibrary('./msdk.dll')
    hdl = objdll.M_Open(1)
    print("open handle = " + str(hdl))
    # objdll.M_MoveTo(hdl, 100, 100)
    res = objdll.M_KeyPress(hdl, 4, 2)
