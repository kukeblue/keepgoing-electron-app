import pyautogui
import sys
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=False, lang="ch")

class MHWindow:
    screenUnit = 2
    windowArea = [0, 0, 0, 0]
    windowAreaGui = (0, 0, 0, 0)
    pyHome = __file__.strip('mhWindow.py')
    pyImageDir = pyHome + 'config/images'

    def __init__(self, screenUnit):
        print('init')
        self.screenUnit = screenUnit

    def getTruthPx(self, num):
        return num * self.screenUnit

    def findMhWindow(self):
        x, y, w, h = self.findPicture('/window_top_left_point.png')
        if(x > 0):
            print(x, y)
            leftx = x - self.getTruthPx(5)
            topy = y - self.getTruthPx(7)
            self.windowArea = [int(leftx / self.screenUnit), int(topy / self.screenUnit), 800, 600]
            self.windowAreaGui = (leftx , topy, self.getTruthPx(800), self.getTruthPx(600))
            print(self.windowAreaGui)
            # pyautogui.screenshot(self.pyImageDir + '/temp/screen.png', region=windowAreaGui)
        else:
            print('未找到前台梦幻窗口')

    def focusWindow(self):
        pyautogui.moveTo(self.windowArea[0] + 400, self.windowArea[1] + 300)
        pyautogui.click()
    
    def F_窗口区域截图(self, fileName, windowRegion):
        region = (windowRegion[0] * self.screenUnit, windowRegion[1] * self.screenUnit, windowRegion[2] * self.screenUnit, windowRegion[3] * self.screenUnit )
        pyautogui.screenshot(self.pyImageDir + '/temp/' + fileName, region=region)
        return self.pyImageDir + '/temp/' + fileName

    def F_截图文字识别(self, path):
        ret = ocr.ocr(path, cls=True)
        str = ''
        if(ret != None):
            for item in ret:
                str = str + item[1][0]
        return str

    def findPicture(self, path):
        return pyautogui.locateOnScreen(self.pyImageDir + path)

    def findImgInWindow(self, path, confidence=0.75):
        location = pyautogui.locateOnScreen(self.pyImageDir + path, region=self.windowAreaGui, confidence=confidence)
        if(location != None):
            return [int(location.left / self.screenUnit), int(location.top / self.screenUnit), int(location.width / self.screenUnit), int(location.height / self.screenUnit)]
        return location

    def checkpoint(self):
        imagePath = '/window_point.png'
        point = self.findImgInWindow(imagePath)
        if point is None:
            self.focusWindow()
            point = self.findImgInWindow(imagePath)
        if point is None:
            self.focusWindow()
            point = self.findImgInWindow(imagePath)
        return point

    def pointMove(self, mx, my):
        finished = False
        while not finished:
            point = self.checkpoint()
            dx = point[0] - 30
            dy = point[1] - 27
            if mx - dx > 5 or mx - dx < -5 or my - dy > 5 or my - dy < -5:
                cx = mx - dx
                cy = my - dy
                pyautogui.move(cx, cy)
            else:
                finished = True

if __name__ == '__main__':
    window = MHWindow(2)
    window.findMhWindow()
    