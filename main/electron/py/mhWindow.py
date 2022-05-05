# coding=utf-8
from asyncio import sleep
from typing_extensions import Self

from cv2 import log
# from matplotlib.pyplot import switch_backend
import logUtil
import pyautogui
import sys
import baiduApi
import time
import utils
import math

mapCangkuDict = {
    '花果山': 25,
    '傲来国': 24,
    '狮驼岭': 23,
    '大唐境外': 22,
    '普陀山': 21,
    '墨家村': 20,
    '北俱芦洲': 19,
    '朱紫国': 18,
    '大唐国境': 17,
    '麒麟山': 16,
    '长寿郊外': 15,
    '东海湾': 14,
    '五庄观': 13,
    '江南野外': 12,
    '建邺城': 11,
    '女儿村': 10,
    # '东海湾': 9,
}


class MHWindow:
    screenUnit = 2
    windowArea = [0, 0, 0, 0]
    windowArea2 = [0, 0, 0, 0]
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
            self.windowArea2 = [int(leftx / self.screenUnit),
                                int(topy / self.screenUnit), int(leftx / self.screenUnit) + 800, int(topy / self.screenUnit) + 600]
            self.windowAreaGui = (
                leftx, topy, self.getTruthPx(800), self.getTruthPx(600))
            print(self.windowAreaGui)
            pyautogui.screenshot(
                self.pyImageDir + '/temp/screen.png', region=self.windowAreaGui)
        else:
            print('未找到前台梦幻窗口')

    def focusWindow(self):
        pyautogui.moveTo(self.windowArea[0] + 450, self.windowArea[1] + 300)

    def F_窗口区域截图(self, fileName, windowRegion):
        region = (windowRegion[0] * self.screenUnit, windowRegion[1] * self.screenUnit,
                  windowRegion[2] * self.screenUnit, windowRegion[3] * self.screenUnit)
        pyautogui.screenshot(self.pyImageDir + '/temp/' +
                             fileName, region=region)
        return self.pyImageDir + '/temp/' + fileName

    def F_截图文字识别(self, path):
        return baiduApi.F_通用文字识别(path)

    def F_宝图文字识别(self, area):
        return baiduApi.F_大漠宝图文字识别(area)

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
            location = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片(img), region=windowArea, confidence=confidence)

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
        for x in range(5):
            print(self.windowArea2)
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '306ca8', '1|0|285490,1|1|285490', 0.6, 0)
            if(ret[1] > 0):
                return (ret[1], ret[2])
            ret2 = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '205890', '0|0|205890', 0.6, 0)
            if(ret2[1] > 0):
                return (ret2[1], ret2[2])

    def ClickInWindow(self, x, y):
        self.pointMove(self.windowArea[0] + x, self.windowArea[1] + y)
        pyautogui.click()

    def pointMove(self, x, y):
        isFirstMove = True
        mx = x - 20
        my = y - 16
        finished = False
        while not finished:
            point = self.checkpoint()
            if(point != None):
                dx = point[0] - 48
                dy = point[1] - 38
                if mx - dx > 2 or mx - dx < -2 or my - dy > 2 or my - dy < -2:
                    cx = mx - dx
                    cy = my - dy
                    if(isFirstMove):
                        pyautogui.move(cx / 1.5, cy / 1.5)
                        isFirstMove = False
                    else:
                        pyautogui.move(cx, cy)
                else:
                    finished = True
            real = pyautogui.position()
            realX = real[0]
            realY = real[1]
            if(realX > (self.windowArea[0] + 800) or realX < self.windowArea[0] or realY > (self.windowArea[1] + 600) or realY < (self.windowArea[1])):
                baiduApi.op.MoveTo(
                    self.windowArea[0] + 400, self.windowArea[1] + 300)

    def F_是否在战斗(self):
        try:
            point = self.findImgInWindow(
                'window_zhandou_mask.png', area=(441, 561, 40, 40))
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
        坐标 = self.获取当前坐标()
        count = 0
        while(True):
            time.sleep(0.5)
            坐标2 = self.获取当前坐标()
            if(坐标2 != None and 坐标 != None and 坐标 == 坐标2):
                if(count > 2):
                    break
                count = count + 1
            else:
                count = 0
                坐标 = 坐标2

    def F_自动战斗(self):
        for i in range(3):
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
        self.focusWindow()
        pyautogui.hotkey('alt', 'e')
        point = self.findImgInWindow('daoju_top.png')
        if(point != None):
            firstBlockX = point[0] + 26
            firstBlockY = point[1] + 83
            left = ((num-1) % 5) * 50
            height = math.floor((num-1) / 5) * 50
            self.pointMove(firstBlockX + left, firstBlockY + height)

    def F_选中仓库道具格子(self, num):
        firstBlockX = self.windowArea[0] + 500
        firstBlockY = self.windowArea[1] + 113
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)

    def F_选中收购商格子(self, num):
        firstBlockX = self.windowArea[0] + 306
        firstBlockY = self.windowArea[1] + 178
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)

    def F_卖装备(self, num):
        for x in range(num):
            self.F_选中收购商格子(x + 1)
            pyautogui.click()
            self.F_移动到游戏区域坐标(404, 444)
            pyautogui.click()
            time.sleep(0.2)
            self.F_移动到游戏区域坐标(206, 338)
            pyautogui.click()
            time.sleep(1)
            pyautogui.click()

    def F_使用飞行符(self, path):
        self.F_选中道具格子(20)
        pyautogui.rightClick()
        time.sleep(1)
        if(path == '傲来国'):
            self.pointMove(self.windowArea[0] + 678, self.windowArea[1] + 423)
            pyautogui.click()
        if(path == '建邺城'):
            self.pointMove(self.windowArea[0] + 527, self.windowArea[1] + 358)
            pyautogui.click()

        pyautogui.hotkey('alt', 'e')

    def F_使用长安城飞行棋(self, path):
        self.F_选中道具格子(16)
        pyautogui.rightClick()
        time.sleep(1)
        if(path == '大唐国境出口'):
            self.pointMove(self.windowArea[0] + 139, self.windowArea[1] + 435)
            pyautogui.click()
        elif(path == '江南野外出口'):
            self.pointMove(self.windowArea[0] + 657, self.windowArea[1] + 435)
            pyautogui.click()
        elif(path == '化生寺出口'):
            self.pointMove(self.windowArea[0] + 627, self.windowArea[1] + 169)
            pyautogui.click()
        pyautogui.hotkey('alt', 'e')

    def F_使用朱紫国飞行棋(self, path):
        self.F_选中道具格子(19)
        pyautogui.rightClick()
        time.sleep(1)
        if(path == '大唐境外出口'):
            self.pointMove(self.windowArea[0] + 198, self.windowArea[1] + 423)
            pyautogui.click()
        if(path == '麒麟山出口'):
            self.pointMove(self.windowArea[0] + 195, self.windowArea[1] + 187)
            pyautogui.click()
        pyautogui.hotkey('alt', 'e')

    def F_使用长寿村飞行棋(self, path):
        self.F_选中道具格子(17)
        pyautogui.rightClick()
        time.sleep(1)
        if(path == '长寿郊外出口'):
            self.pointMove(self.windowArea[0] + 503, self.windowArea[1] + 465)
            pyautogui.click()
        pyautogui.hotkey('alt', 'e')

    def F_使用傲来国飞行棋(self, path):
        self.F_选中道具格子(18)
        pyautogui.rightClick()
        time.sleep(1)
        if(path == '花果山出口'):
            self.pointMove(self.windowArea[0] + 584, self.windowArea[1] + 180)
            pyautogui.click()
        if(path == '女儿村出口'):
            self.pointMove(self.windowArea[0] + 208, self.windowArea[1] + 188)
            pyautogui.click()
        if(path == '东海湾出口'):
            self.pointMove(self.windowArea[0] + 519, self.windowArea[1] + 399)
            pyautogui.click()
        pyautogui.hotkey('alt', 'e')

    def F_导航到大唐国境(self):
        self.F_使用长安城飞行棋('大唐国境出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 25, self.windowArea[1] + 441)
        pyautogui.click()
        time.sleep(3)

    def F_导航到江南野外(self):
        self.F_使用长安城飞行棋('江南野外出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 726, self.windowArea[1] + 515)
        pyautogui.click()
        time.sleep(3)

    def F_导航到狮驼岭(self):
        self.F_使用朱紫国飞行棋('大唐境外出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 76, self.windowArea[1] + 560)
        pyautogui.click()
        time.sleep(1)
        time.sleep(2)
        self.pointMove(self.windowArea[0] + 80, self.windowArea[1] + 565)
        pyautogui.click()
        time.sleep(5)

    def F_导航到大唐境外(self):
        self.F_使用朱紫国飞行棋('大唐境外出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 76, self.windowArea[1] + 560)
        pyautogui.click()
        time.sleep(1)

    def F_导航到墨家村(self):
        self.F_使用朱紫国飞行棋('大唐境外出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 76, self.windowArea[1] + 560)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 322, self.windowArea[1] + 259)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(40)
        self.pointMove(self.windowArea[0] + 403, self.windowArea[1] + 137)
        pyautogui.press('f9')
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 386, self.windowArea[1] + 143)
        pyautogui.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 211, self.windowArea[1] + 337)
        pyautogui.click()
        time.sleep(1)

    def F_导航到麒麟山(self):
        self.F_使用朱紫国飞行棋('麒麟山出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 35, self.windowArea[1] + 125)
        pyautogui.click()
        time.sleep(3)

    def F_导航到长寿郊外(self):
        self.F_使用长寿村飞行棋('长寿郊外出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 634, self.windowArea[1] + 518)
        pyautogui.click()
        time.sleep(4)

    def F_导航到傲来国(self):
        self.F_使用飞行符('傲来国')
        time.sleep(1)

    def F_导航到建邺城(self):
        self.F_使用飞行符('建邺城')
        time.sleep(1)

    def F_导航到东海湾(self):
        self.F_使用傲来国飞行棋('东海湾出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 221, self.windowArea[1] + 362)
        pyautogui.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 208, self.windowArea[1] + 336)
        pyautogui.click()
        time.sleep(1)

    def F_导航到花果山(self):
        self.F_使用傲来国飞行棋('花果山出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 768, self.windowArea[1] + 84)
        pyautogui.click()
        time.sleep(4)

    def F_导航到花果山(self):
        self.F_使用傲来国飞行棋('花果山出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 768, self.windowArea[1] + 84)
        pyautogui.click()
        time.sleep(4)

    def F_导航到女儿村(self):
        self.F_使用傲来国飞行棋('女儿村出口')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 50, self.windowArea[1] + 131)
        pyautogui.click()
        time.sleep(3)

    def F_导航到北俱芦洲(self):
        self.F_导航到长寿郊外()

        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 303, self.windowArea[1] + 344)
        pyautogui.click()
        time.sleep(26)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 273)
        pyautogui.doubleClick()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 207, self.windowArea[1] + 340)
        pyautogui.click()
        time.sleep(1)

    def F_导航到朱紫国(self):
        self.F_使用朱紫国飞行棋('大唐境外出口')
        time.sleep(1)

    def F_导航到普陀山(self):
        self.F_导航到大唐国境()
        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 416, self.windowArea[1] + 426)
        pyautogui.click()
        time.sleep(30)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 304)
        pyautogui.doubleClick()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 206, self.windowArea[1] + 339)
        pyautogui.click()
        time.sleep(1)

    def F_移动到游戏区域坐标(self, x, y):
        self.pointMove(self.windowArea[0] + x, self.windowArea[1] + y)

    def F_选择仓库号(self, num):
        if(num == 1):
            self.F_移动到游戏区域坐标(180, 307)
        if(num == 8):
            self.F_移动到游戏区域坐标(180, 350)
        elif(num == 9):
            self.F_移动到游戏区域坐标(200, 350)
        elif(num == 10):
            self.F_移动到游戏区域坐标(220, 350)
        elif(num == 11):
            self.F_移动到游戏区域坐标(240, 350)
        elif(num == 12):
            self.F_移动到游戏区域坐标(260, 350)
        elif(num == 13):
            self.F_移动到游戏区域坐标(280, 350)
        elif(num == 14):
            self.F_移动到游戏区域坐标(300, 350)
        elif(num == 15):
            self.F_移动到游戏区域坐标(320, 350)
        elif(num == 16):
            self.F_移动到游戏区域坐标(340, 350)
        elif(num == 17):
            self.F_移动到游戏区域坐标(180, 374)
        elif(num == 18):
            self.F_移动到游戏区域坐标(200, 374)
        elif(num == 19):
            self.F_移动到游戏区域坐标(228, 374)
        elif(num == 20):
            self.F_移动到游戏区域坐标(248, 374)
        elif(num == 21):
            self.F_移动到游戏区域坐标(263, 371)
        elif(num == 22):
            self.F_移动到游戏区域坐标(288, 374)
        elif(num == 23):
            self.F_移动到游戏区域坐标(308, 374)
        elif(num == 24):
            self.F_移动到游戏区域坐标(329, 374)
        elif(num == 25):
            self.F_移动到游戏区域坐标(348, 374)
        pyautogui.click()

    def F_回天台放东西(self, map):
        self.F_选中道具格子(20)
        pyautogui.rightClick()
        self.pointMove(self.windowArea[0] + 507, self.windowArea[1] + 282)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        self.F_移动到游戏区域坐标(267, 188)
        pyautogui.click()
        pyautogui.click()
        time.sleep(3)
        self.F_移动到游戏区域坐标(283, 352)
        pyautogui.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(227, 373)
        pyautogui.click()
        # # 8号仓库
        time.sleep(1)
        num = mapCangkuDict.get(map)
        self.F_选择仓库号(num)
        time.sleep(1)
        for x in range(15):
            self.F_选中仓库道具格子(x + 1)
            pyautogui.rightClick()
        self.F_选择仓库号(1)
        time.sleep(1)
        self.F_移动到游戏区域坐标(198, 110)
        pyautogui.rightClick()
        time.sleep(1)
        self.F_选中道具格子(1)
        pyautogui.rightClick()
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        self.F_选中仓库道具格子(1)
        pyautogui.rightClick()
        self.F_移动到游戏区域坐标(720, 35)
        pyautogui.rightClick()

    def 获取当前坐标(self):
        ret = baiduApi.F_大漠坐标文字识别([self.windowArea[0], self.windowArea[1],
                                   self.windowArea[0] + 143,  self.windowArea[1] + 47])
        if(ret != None):
            str = ret.replace(",", "")
            return str


if __name__ == '__main__':
    window = MHWindow(1, '12')
    window.findMhWindow()
    window.focusWindow()
    time.sleep(1)
    window.F_卖装备(15)
    # print(window.F_是否结束寻路())
