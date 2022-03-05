import win32api
import win32gui
import time
import pyautogui
import os
from win32com.client import Dispatch
op=Dispatch("op.opsoft")


op.moveTo(80, 100)
pyautogui.click()
time.sleep(3)
print('finish')