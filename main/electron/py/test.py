import time
from win32com.client import Dispatch
import win32api
import utils
import sys
import os
import logUtil
op = Dispatch("op.opsoft")

pyHome = __file__.strip('test.py')
pyZhikuDir = pyHome + 'config/zhiku'

op.SetDict(0, pyZhikuDir + '/baotuzuobiao.txt')
s = op.Ocr(283, 29, 968, 614, "00ff00-000000", 1.0)
print(s)
