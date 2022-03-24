# coding=utf-8
import logUtil
import pyautogui
import sys
import baiduApi


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

    def findImgInWindow(self, img, confidence=0.75):
        location = None
        if(confidence == None):
            location = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片(img), region=self.windowAreaGui, grayscale=False)
        else:
            location = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片(img), region=self.windowAreaGui, confidence=confidence)

        if(location != None):
            return [int(location.left / self.screenUnit), int(location.top / self.screenUnit), int(location.width / self.screenUnit), int(location.height / self.screenUnit)]
        return location

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

    def pointMove(self, mx, my):
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


if __name__ == '__main__':
    window = MHWindow(2, '1')
    window.findMhWindow()
