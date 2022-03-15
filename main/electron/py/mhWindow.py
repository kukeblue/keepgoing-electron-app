import pyautogui
import sys

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
        x, y, w, h = self.findPicture('/test_image.png')
        if(x > 0):
            print(x, y)
            leftx = x - self.getTruthPx(7)
            topy = y - self.getTruthPx(7)
            self.windowArea = [leftx, topy, self.getTruthPx(800), self.getTruthPx(600)]
            windowAreaGui = (leftx , topy, self.getTruthPx(800), self.getTruthPx(600))
            print(windowAreaGui)
            pyautogui.screenshot(self.pyImageDir + '/temp/screen.png', region=windowAreaGui)
        else:
            print('未找到前台梦幻窗口')


    def findPicture(self, path):
        return pyautogui.locateOnScreen(self.pyImageDir + path)


if __name__ == '__main__':
    window = MHWindow(2)
    window.findMhWindow()
    