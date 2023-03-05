# coding=utf-8
import random
import logUtil
import sys
import io
import time
import utils
import pyautogui
import utils
import mhWindow
from tkinter import messagebox
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
from winsound import PlaySound

pyHome = __file__.strip('baiduApi.pyc')
pyZhikuDir = pyHome + 'config\zhiku'
pyZhikuDir2 = pyHome + 'config\images'
pyZhikuDir3 = pyHome + '\config'



def F_碗子山找怪(window):
    pyautogui.press('f9')
    pics = ['all-wzs-xz-1.png', 
            'all-wzs-xz-2.png',
            'all-wzs-xz-3.png',
            'all-wzs-xz-4.png',
            # 'all-wzs-mm-1.png',
            'all-wzs-hd-1.png',
            # 'all-wzs-hd-4.png',
            'all-wzs-hl-1.png',
            'all-wzs-hl-2.png',
            'all-wzs-hl-4.png',
            'all-wzs-hl-5.png',
            'all-wzs-hl-6.png',
            'all-wzs-hl-7.png',
            'all-wzs-hl-8.png',
            'all-wzs-hl-9.png',
            'all-wzs-kb-2.png',
            'all-wzs-kb-5.png',
            'all-wzs-kb-6.png',
            'all-wzs-kb-4.png',
            'all-wzs-kb-7.png',
            'all-wzs-kb-8.png',
            ]
    for pic in pics:
        point = window.findImgInWindow(pic, confidence=0.93)
        if(point == None):
            point = window.findImgInWindow(pic, confidence=0.91)
            if(point == None):
                point = window.findImgInWindow(pic, confidence=0.90)
        if(point != None):
            print(pic)
            window.pointMove(point[0], point[1])
            PlaySound("C:\\y913.wav", flags=1)
            time.sleep(5)
            return point
            


def F_碗子山巡逻(window):
    logUtil.chLog('F_碗子山巡逻')
    points = [[326, 266], [329, 196], [388, 200], [
        412, 266], [428, 320], [400, 391], [325, 383], [384, 470], [325, 478]]
    lastPoint = None
    time.sleep(1)
    _index = 1
    while True:
        _index = _index + 1
        if(_index == 10):
            time.sleep(30)
            _index = 1
        index = 9 - _index
        point = points[index]
        if(lastPoint == point):
            continue
        pyautogui.press('tab')
        window.F_移动到游戏区域坐标(point[0] + random.choice((-1, 1)) * random.randint(
            1, 20), point[1] + random.choice((-1, 1)) * random.randint(1, 20), True)
        utils.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        window.F_是否结束寻路()
        point = F_碗子山找怪(window)
        if(point != None):
            break
     
MHWindow = mhWindow.MHWindow
window = MHWindow(1)
window.findMhWindow()
# F_碗子山巡逻(window)
F_碗子山找怪(window)


