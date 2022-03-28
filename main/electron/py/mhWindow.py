# coding=utf-8
from typing_extensions import Self

from cv2 import log
import logUtil
import pyautogui
import sys
import baiduApi
import time
import utils
import math


class MHWindow:
    screenUnit = 2
    windowArea = [0, 0, 0, 0]
    windowAreaGui = (0, 0, 0, 0)
    pyHome = __file__.strip('mhWindow.py')
    pyImageDir = pyHome + 'config\images'
    deviceId = ''

    def __init__(self, screenUnit, deviceId):
        print('init')
        self.screenUnit = screenUnit
        self.deviceId = deviceId

    def F_获取设备图片(self, img):
        print('\\' + self.deviceId + '-' + img)
        return '\\' + self.deviceId + '-' + img

    def getTruthPx(self, num):
        return num * self.screenUnit

    def findMhWindow(self):
        x, y, w, h = self.findPicture('window_top_left_point.png')
        if(x > 0):
            print(x, y)
            leftx = x - self.getTruthPx(5)
            topy = y - self.getTruthPx(7)
            self.windowArea = [int(leftx / self.screenUnit),
                               int(topy / self.screenUnit), 800, 600]
            self.windowAreaGui = (
                leftx, topy, self.getTruthPx(800), self.getTruthPx(600))
            print(self.windowAreaGui)
            pyautogui.screenshot(self.pyImageDir + '/temp/screen.png', region=self.windowAreaGui)
        else:
            print('未找到前台梦幻窗口')

    def focusWindow(self):
        pyautogui.moveTo(self.windowArea[0] + 400, self.windowArea[1] + 300)
        pyautogui.click()

    def F_窗口区域截图(self, fileName, windowRegion):
        region = (windowRegion[0] * self.screenUnit, windowRegion[1] * self.screenUnit,
                  windowRegion[2] * self.screenUnit, windowRegion[3] * self.screenUnit)
        pyautogui.screenshot(self.pyImageDir + '/temp/' +
                             fileName, region=region)
        return self.pyImageDir + '/temp/' + fileName

    def F_截图文字识别(self, path):
        return baiduApi.F_通用文字识别(path)
    
    def findPicture(self, img):
        return pyautogui.locateOnScreen(self.pyImageDir + self.F_获取设备图片(img))

    def findImgInWindow(self, img, confidence=0.75, area=(0, 0, 0, 0)):
        location = None
        windowArea = None
        if(area[0] != 0):
            x = self.windowAreaGui[0] + area[0]
            y = self.windowAreaGui[1] + area[1]
            width = area[2]
            height = area[3]
            windowArea = (x, y, width, height)
        else:
            windowArea = self.windowAreaGui
        if(confidence == None):
            location = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片(img), region=windowArea, grayscale=False)
        else:
            location = pyautogui.locateOnScreen(self.pyImageDir + self.F_获取设备图片(img), region=windowArea, confidence=confidence)

        if(location != None):
            return [int(location.left / self.screenUnit), int(location.top / self.screenUnit), int(location.width / self.screenUnit), int(location.height / self.screenUnit)]
        return location

    def findImgInWindowReturnWindowPoint(self, img, confidence=0.75, area=(0, 0, 0, 0)):
        point = self.findImgInWindow(img, confidence=0.75, area=(0, 0, 0, 0))
        if(point != None):
            point[0] = point[0] - self.windowArea[0]
            point[1] = point[1] - self.windowArea[1]
            return point

    def findImgsInWindow(self, img):
        locations = pyautogui.locateAllOnScreen(
            self.pyImageDir + self.F_获取设备图片(img), region=self.windowAreaGui, grayscale=False)
        ponits = []
        for location in locations:
            ponits.append([int(location.left / self.screenUnit), int(location.top / self.screenUnit),
                          int(location.width / self.screenUnit), int(location.height / self.screenUnit)])
        return ponits

    def checkpoint(self):
        imagePath = 'window_point.png'
        point = self.findImgInWindow(imagePath)
        if point is None:
            self.focusWindow()
            point = self.findImgInWindow(imagePath)
        if point is None:
            self.focusWindow()
            point = self.findImgInWindow(imagePath)
        return point

    def ClickInWindow(self, x, y):
        self.pointMove(self.windowArea[0] + x, self.windowArea[1] + y)
        pyautogui.click()

    def pointMove(self, x, y):
        mx = x - 15
        my = y - 17
        finished = False
        while not finished:
            point = self.checkpoint()
            if(point != None):
                dx = point[0] - 30
                dy = point[1] - 27
                if mx - dx > 2 or mx - dx < -2 or my - dy > 2 or my - dy < -2:
                    cx = mx - dx
                    cy = my - dy
                    pyautogui.move(cx, cy)
                else:
                    finished = True
            else:
                self.focusWindow()

    def F_是否在战斗(self):
        try:
            point =self.findImgInWindow('window_zhandou_mask.png', area=(441, 561, 40, 40))
            if point != None:
                print('F_是否在战斗： 是')
                return True
            else:
                print('F_是否在战斗： 否')
                return False
        except:
            print('F_是否在战斗： 是')
            return False
    
    def F_识别当前坐标(self):
        位置信息 = [self.windowArea[0], self.windowArea[1] + 19, 124, 52]
        # 截图 + ocr识别
        path = self.F_窗口区域截图('temp_zuobiao_info.png', 位置信息)
        time.sleep(1)
        ret = utils.F_本地文字识别(path)
        return ret

    def F_是否结束寻路(self):
        当前坐标 = self.F_识别当前坐标()
        count = 0
        while(True):
            坐标 = self.F_识别当前坐标()
            print('F_是否结束寻路', 当前坐标, 坐标)
            if(当前坐标 == 坐标):
                break
            else:
               当前坐标 = 坐标
            count = count + 1


    def F_自动战斗(self):
        for i in range(20):
            print('F_自动战斗：等待进入战斗:' + str(i))
            time.sleep(1)
            if(self.F_是否在战斗()):
                print('F_自动战斗：进入战斗')
                while(True):
                   time.sleep(1)
                   if(self.F_是否在战斗() == False):
                       print('F_自动战斗：结束战斗')
                       break
    
    def F_选中道具格子(self, num):
        point = self.findImgInWindow('daoju_top.png')
        if(point != None):
            firstBlockX = point[0] + 26
            firstBlockY = point[1] + 83
            left = ((num-1) % 5) * 50
            height = math.floor((num-1) / 5) * 50
            self.pointMove(firstBlockX + left, firstBlockY + height)

if __name__ == '__main__':
    window = MHWindow(1, '11')
    window.findMhWindow()
    window.focusWindow()
    time.sleep(1)
