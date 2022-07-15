# coding=utf-8
from distutils.log import error
from tkinter.messagebox import NO
from cv2 import log
import logUtil
import pyautogui
import pydirectinput
import sys
import baiduApi
import networkApi
import time
import utils
import math
import re
import pointUtil
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

傲来国坐标点 = {
    '黄色傲来国导标旗坐标_女儿村': [6, 138],
}

记录值 = {
    '满仓库遍历值': 2,
    '仓库位置': '长安城',
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
        if('all' in img):
            return '\\' + img
        print('\\' + '9' + '-' + img)
        return '\\' + '9' + '-' + img

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
            # pyautogui.screenshot(
            #     self.pyImageDir + '/temp/screen.png', region=self.windowAreaGui)
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
            self.pyImageDir + self.F_获取设备图片(img), region=self.windowAreaGui, grayscale=False, confidence=0.75)
        ponits = []
        for location in locations:
            ponits.append([int(location.left / self.screenUnit), int(location.top / self.screenUnit),
                          int(location.width / self.screenUnit), int(location.height / self.screenUnit)])
        return ponits

    def checkpoint(self, 战斗操作模式=False, 手指操作模式=False):
        for x in range(3):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '306ca8', '1|0|285490,1|1|285490', 0.6, 0)
            if(ret[1] > 0):
                return (ret[1], ret[2])
            ret2 = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '205890', '0|0|205890', 0.6, 0)
            if(ret2[1] > 0):
                return (ret2[1], ret2[2])
        if(战斗操作模式):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '884448', '4|4|f0ecb8,1|2|401c28,-1|-2|a84048,-4|-3|f0f8f0', 0.6, 0)
            if(ret[1] > 0):
                return (ret[1], ret[2])
        if(手指操作模式):
            for x in range(2):
                ret = baiduApi.op.FindMultiColor(
                    self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], 'd86c30', '0|1|d86c30,1|4|c85030,6|-2|200000', 0.5, 0)
                if(ret[1] > 0):
                    return (ret[1], ret[2])

    def ClickInWindow(self, x, y):
        self.pointMove(self.windowArea[0] + x, self.windowArea[1] + y)
        pydirectinput.click()

    def pointMove(self, x, y, 战斗操作模式=False, 手指操作模式=False):
        isFirstMove = 0
        mx = x - 20
        my = y - 16
        safeAreaLeft = self.windowArea2[0] + 100
        safeAreaRight = self.windowArea2[0] + 700
        safeAreaTop = self.windowArea2[1] + 100
        safeAreaBottom = self.windowArea2[1] + 500
        isSafeArea = False
        if(mx > safeAreaLeft and mx > safeAreaRight and my < safeAreaBottom and my  > safeAreaTop):
            isSafeArea = True
        finished = False
        while not finished:
            point = self.checkpoint(战斗操作模式=战斗操作模式, 手指操作模式=手指操作模式)
            if(point != None):
                dx = point[0] - 48
                dy = point[1] - 38
                if mx - dx > 2 or mx - dx < -2 or my - dy > 2 or my - dy < -2:
                    cx = mx - dx
                    cy = my - dy
                    if(isFirstMove < 1):
                        pyautogui.move(cx / 2, cy / 2)
                        isFirstMove = isFirstMove + 1
                    else:
                        if(isSafeArea):
                            pyautogui.move(cx, cy)
                        else:
                            if(cx > 40):
                                cx = 40
                            elif(cx < -40):
                                cx = -40
                            if(dy > 30):
                                dy = 30
                            elif(dy < -30):
                                dy = -30
                            pyautogui.move(cx, cy)
                else:
                    finished = True
            real = pyautogui.position()
            realX = real[0]
            realY = real[1]
            if(realX > (self.windowArea[0] + 800) or realX < self.windowArea[0] or realY > (self.windowArea[1] + 600) or realY < (self.windowArea[1])):
                baiduApi.op.MoveTo(
                    self.windowArea[0] + 400, self.windowArea[1] + 300)
                time.sleep(1)

    def F_是否在战斗(self):
        try:
            point = self.findImgInWindow(
                'window_zhandou_mask.png', area=(441, 561, 40, 40))
            if point != None:
                return True
            else:
                return False
        except:
            return False

    def F_是否战斗操作(self):
        try:
            point = self.findImgInWindow(
                'all-zhandou-taopao.png', area=(600, 101, 200, 469))
            if point != None:
                return True
            else:
                return False
        except:
            return False

    def F_是否结束战斗(self):
        try:
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0]+380, self.windowArea2[1]+520, self.windowArea2[0]+545, self.windowArea2[1]+600, 'c80000', '5|3|882800,8|2|881400,5|4|882800', 0.8, 0)
            if ret[1] > 0:
                return True
            else:
                return False
        except:
            return False

    def F_吃药(self):
        pyautogui.hotkey('alt', 'e')
        try:
            point = self.findImgInWindow(
                'all_lanwan.png', area=(97, 438, 149, 495))
            if point != None:
                self.pointMove(point[0], point[1])
                pydirectinput.click(button="right")
            point = self.findImgInWindow(
                'all_hongwan.png', area=(149, 438, 200, 495))
            if point != None:
                self.pointMove(point[0], point[1])
                pydirectinput.click(button="right")
        except:
            print('F_吃药 error')
        pyautogui.hotkey('alt', 'e')

    def F_识别当前坐标(self):
        位置信息 = [self.windowArea[0], self.windowArea[1] + 19, 124, 52]
        # 截图 + ocr识别
        path = self.F_窗口区域截图('temp_zuobiao_info.png', 位置信息)
        time.sleep(1)
        ret = utils.F_本地文字识别(path)
        return ret

    def F_识别当前任务(self):
        位置信息 = [self.windowArea[0] + 640, self.windowArea[1] + 110,
                163, 133]
        # 截图 + ocr识别
        path = self.F_窗口区域截图('temp_renwu_info.png', 位置信息)
        time.sleep(1)
        ret = utils.F_通用文字识别(path)
        return ret

    def F_识别自定义任务(self):
        位置信息 = [self.windowArea[0] + 342, self.windowArea[1] + 76,
                211, 105]
        # 截图 + ocr识别
        path = self.F_窗口区域截图('temp_zidingyi_renwu_info.png', 位置信息)
        time.sleep(1)
        ret = utils.F_通用文字识别(path)
        return ret

    def F_识别4小人(self):
        ret = baiduApi.F_大漠红色4小人弹框识别([self.windowArea[0], self.windowArea[1],
                                     self.windowArea[0] + 600, self.windowArea[1] + 800])
        if(ret != None):
            x = ret[0]-30
            y = ret[1]-30
            位置信息 = [x, y,
                    400, 200]
            print("找到")
            path = self.F_窗口区域截图('temp_4_person_info.png', 位置信息)
            time.sleep(1)
            data = networkApi.getPicPoint(path)
            if(data != '' and "," in data):
                clickPoints = data.split(',')
                if(clickPoints[1]):
                    print('success')
                    return True
            else:
                print("识别失败")
        else:
            print("未找到")

    def F_是否结束寻路(self):
        坐标 = self.获取当前坐标()
        count = 0
        while(True):
            time.sleep(0.5)
            坐标2 = self.获取当前坐标()
            if(坐标2 != None and 坐标 != None and 坐标 == 坐标2):
                if(count > 1):
                    break
                count = count + 1
            else:
                count = 0
                坐标 = 坐标2

    def F_点击战斗(self, 多次点击=False):
        self.F_移动到游戏区域坐标(574, 442)
        pyautogui.hotkey('alt', 'a')
        pydirectinput.click(button="right")
        while True:
            point = self.findImgInWindow('all-duibiao.png')
            if(point == None):
                point = self.findImgInWindow('all-duibiao-plus.png')
            if(point != None):
                pyautogui.hotkey('alt', '7')
                time.sleep(0.5)
                self.pointMove(point[0]+5, point[1] + 78)
                pyautogui.hotkey('alt', 'a')
                time.sleep(0.1)
                if(多次点击):
                    time.sleep(2)
                    pydirectinput.doubleClick()
                    pydirectinput.click()
                else:
                    pydirectinput.click()
                break
            time.sleep(0.5)

    def F_自动战斗(self):
        pyautogui.press('f9')
        for i in range(4):
            print('F_自动战斗：等待进入战斗:' + str(i))
            time.sleep(1)
            if(self.F_是否在战斗()):
                print('F_自动战斗：进入战斗')
                while(True):
                    time.sleep(1)
                    if(self.F_是否结束战斗()):
                        print('F_自动战斗：结束战斗')
                        break

    def F_自动战斗2(self):
        finish = False
        while(finish == False):
            time.sleep(1)
            if(self.F_是否在战斗()):
                while(True):
                    time.sleep(1)
                    if(self.F_是否在战斗() == False):
                        finish = True
                        break

    def F_选中道具格子(self, num):
        self.focusWindow()
        point = self.findImgInWindow('daoju_top.png')
        if(point == None):
            pyautogui.hotkey('alt', 'e')
            time.sleep(0.5)
        point = self.findImgInWindow('daoju_top.png')
        firstBlockX = point[0] + 26
        firstBlockY = point[1] + 83
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)
        return

    def F_选中道具格子2(self, num):

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
            pydirectinput.click()
            self.F_移动到游戏区域坐标(404, 440)
            pydirectinput.click()
            time.sleep(0.5)
            self.F_移动到游戏区域坐标(206, 338)
            pydirectinput.click()
            time.sleep(0.5)
            pydirectinput.click()

    def F_丢垃圾(self, num):
        self.focusWindow()
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        for x in range(num):
            self.F_选中道具格子2(x + 1)
            pydirectinput.click()
            self.F_移动到游戏区域坐标(376, 344)
            pydirectinput.click()
            time.sleep(0.5)
            self.F_移动到游戏区域坐标(356, 344)
            pydirectinput.click()

    def F_使用飞行符(self, path):
        desLocation = ""
        if(path == '傲来国'):
            desLocation = pointUtil.傲来国飞行符坐标_飞行棋Str
        elif(path == '建邺城'):
            desLocation = pointUtil.建邺城飞行符坐标_飞行棋Str
        elif(path == '宝象国'):
            desLocation = pointUtil.宝象国飞行符坐标_飞行棋Str
        elif(path == '长寿村'):
            desLocation = pointUtil.长寿村飞行符坐标_飞行棋Str
        elif(path == '西梁女国'):
            desLocation = pointUtil.西凉女国飞行符坐标_飞行棋Str
        elif(path == '长安城'):
            desLocation = pointUtil.长安城飞行符坐标_飞行棋Str
        elif(path == '朱紫国'):
            desLocation = pointUtil.朱紫国飞行符坐标_飞行棋Str
        while(True):
            curLocation = self.获取当前坐标()
            if(curLocation in desLocation):
                break
            else:
                if (self.findImgInWindow("all-wind.png") != None):
                    if(path == '傲来国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.傲来国飞行符坐标_屏幕xy[0], pointUtil.傲来国飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    if(path == '长安城'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.长安城飞行符坐标_屏幕xy[0], pointUtil.长安城飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    if(path == '朱紫国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.朱紫国飞行符坐标_屏幕xy[0], pointUtil.朱紫国飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    elif(path == '建邺城'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.建邺城飞行符坐标_屏幕xy[0], pointUtil.建邺城飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    elif(path == '宝象国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.宝象国飞行符坐标_屏幕xy[0], pointUtil.宝象国飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    elif(path == '西梁女国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.西凉女国飞行符坐标_屏幕xy[0], pointUtil.西凉女国飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    elif(path == '长寿村'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.长寿村飞行符坐标_屏幕xy[0], pointUtil.长寿村飞行符坐标_屏幕xy[1])
                        pydirectinput.click()
                    time.sleep(1)
                else:
                    self.F_选中道具格子(20)
                    pydirectinput.click(button="right")
                    time.sleep(1)
        pyautogui.hotkey('alt', 'e')

    def F_使用长安城飞行棋(self, path):
        navWay = ""
        desLocation = ""
        if(path == '大唐国境出口'):
            desLocation = pointUtil.红色长安城导标旗坐标_大唐国境Str
        elif(path == '长安驿站'):
            desLocation = pointUtil.红色长安城导标旗坐标_驿站Str
        elif(path == '江南野外出口'):
            desLocation = pointUtil.红色长安城导标旗坐标_江南野外Str
        elif(path == '化生寺出口'):
            desLocation = pointUtil.红色长安城导标旗坐标_化生寺Str
        while(True):
            curLocation = self.获取当前坐标()
            if(desLocation == curLocation):
                break
            else:
                if (navWay and self.findImgInWindow("all-caqi.png") != None):
                    if(path == '大唐国境出口'):
                        self.pointMove(
                            self.windowArea[0] + 139, self.windowArea[1] + 435)
                        pydirectinput.click()
                    if(path == '长安驿站'):
                        self.pointMove(
                            self.windowArea[0] + 407, self.windowArea[1] + 398)
                        pydirectinput.click()
                    elif(path == '江南野外出口'):
                        self.pointMove(
                            self.windowArea[0] + 657, self.windowArea[1] + 435)
                        pydirectinput.click()
                    elif(path == '化生寺出口'):
                        self.pointMove(
                            self.windowArea[0] + 627, self.windowArea[1] + 169)
                        pydirectinput.click()
                    time.sleep(1)
                    pyautogui.hotkey('alt', 'e')
                    break
                elif(navWay == False):
                    self.F_使用飞行符('长安城')
                    if(path == '大唐国境出口'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_大唐国境, True)
                    elif(path == '长安驿站'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_驿站, True)
                    elif(path == '江南野外出口'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_江南野外, None)
                    elif(path == '化生寺出口'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_化生寺, None)
                    break
                else:
                    pyautogui.hotkey('alt', 'e')
                    time.sleep(1)
                    if (self.findImgInWindow("all-caqi.png") != None):
                        navWay = True
                        self.F_选中道具格子(16)
                        pydirectinput.click(button="right")
                    else:
                        navWay = False
                        pyautogui.hotkey('alt', 'e')
                    time.sleep(1)

    def F_使用朱紫国飞行棋(self, path):
        navWay = True
        desLocation = ""
        if(path == '白色朱紫国导标旗坐标_大唐境外'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_大唐境外Str
        elif(path == '白色朱紫国导标旗坐标_麒麟山'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_麒麟山Str
        elif(path == '白色朱紫国导标旗坐标_妖怪亲信'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_妖怪亲信Str
        elif(path == '白色朱紫国导标旗坐标_酒店'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_酒店Str
        elif(path == '白色朱紫国导标旗坐标_申太公'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_申太公Str
        elif(path == '白色朱紫国导标旗坐标_小团团'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_小团团Str
        elif(path == '白色朱紫国导标旗坐标_紫阳药师附近'):
            desLocation = pointUtil.白色朱紫国导标旗坐标_紫阳药师附近Str
        elif(path == '朱紫国飞行符坐标_飞行符'):
            self.F_导航到朱紫国()
            return
        while(True):
            curLocation = self.获取当前坐标()
            if(desLocation == curLocation):
                break
            else:
                if (navWay and self.findImgInWindow("all-feixing-zz.png") != None):
                    time.sleep(0.5)
                    if(path == '白色朱紫国导标旗坐标_大唐境外'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_大唐境外屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_大唐境外屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_麒麟山'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_麒麟山屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_麒麟山屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_妖怪亲信'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_妖怪亲信屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_妖怪亲信屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_酒店'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_酒店屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_酒店屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_申太公'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_申太公屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_申太公屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_小团团'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_小团团屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_小团团屏幕xy[1])
                    elif(path == '白色朱紫国导标旗坐标_紫阳药师附近'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.白色朱紫国导标旗坐标_紫阳药师附近屏幕xy[0], pointUtil.白色朱紫国导标旗坐标_紫阳药师附近屏幕xy[1])
                    if(path == '朱紫国飞行符坐标_飞行符'):
                        # self.F_导航到朱紫国()
                        print()
                    else:
                        pydirectinput.click()
                        time.sleep(1)
                        pyautogui.hotkey('alt', 'e')
                    break
                elif(navWay == False):
                    self.F_导航到朱紫国()
                    if('朱紫国飞行符坐标_飞行符' != path):
                        if(path == '白色朱紫国导标旗坐标_大唐境外'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_大唐境外)
                        elif(path == '白色朱紫国导标旗坐标_麒麟山'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_麒麟山)
                        elif(path == '白色朱紫国导标旗坐标_妖怪亲信'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_妖怪亲信)
                        elif(path == '白色朱紫国导标旗坐标_酒店'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_酒店)
                        elif(path == '白色朱紫国导标旗坐标_申太公'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_申太公)
                        elif(path == '白色朱紫国导标旗坐标_小团团'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_小团团)
                        elif(path == '白色朱紫国导标旗坐标_紫阳药师附近'):
                            self.F_小地图寻路器(pointUtil.白色朱紫国导标旗坐标_紫阳药师附近)
                        break
                    break
                else:
                    pyautogui.hotkey('alt', 'e')
                    time.sleep(1)
                    if (self.findImgInWindow("all-zzqi.png") != None):
                        self.F_选中道具格子(19)
                        navWay = True
                        pydirectinput.click(button="right")
                        time.sleep(0.5)
                    else:
                        navWay = False
                        pyautogui.hotkey('alt', 'e')
                    time.sleep(1)

    def F_使用长寿村飞行棋(self, path):
        navWay = True
        desLocation = ""
        if(path == '绿色长寿村导标旗坐标_长寿郊外'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_长寿郊外Str
        elif(path == '绿色长寿村导标旗坐标_方寸山'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_方寸山Str
        elif(path == '绿色长寿村导标旗坐标_酒店'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_酒店Str
        elif(path == '绿色长寿村导标旗坐标_当铺'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_当铺Str
        elif(path == '绿色长寿村导标旗坐标_村长家'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_村长家Str
        elif(path == '绿色长寿村导标旗坐标_孟婆婆'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_孟婆婆Str
        elif(path == '绿色长寿村导标旗坐标_钟书生'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_钟书生Str
        elif(path == '绿色长寿村导标旗坐标_酒店'):
            desLocation = pointUtil.绿色长寿村导标旗坐标_酒店Str
        elif(path == '长寿村飞行符坐标_飞行符'):
            self.F_导航到长寿村()
            return
        while(True):
            curLocation = self.获取当前坐标()
            if(desLocation in curLocation):
                break
            else:
                if (navWay and self.findImgInWindow("all-feixing-cs.png") != None):
                    if(path == '绿色长寿村导标旗坐标_长寿郊外'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_长寿郊外屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_长寿郊外屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_方寸山'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_方寸山屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_方寸山屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_酒店'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_酒店屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_酒店屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_当铺'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_当铺屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_当铺屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_村长家'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_村长家屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_村长家屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_钟书生'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_孟婆婆屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_孟婆婆屏幕xy[1])
                    if(path == '长寿村飞行符坐标_飞行符'):
                        self.F_导航到长寿村()
                    else:
                        pydirectinput.click()
                        time.sleep(0.5)
                        pyautogui.hotkey('alt', 'e')
                        break
                elif(navWay == False):
                    self.F_导航到长寿村()
                    time.sleep(1)
                    if(path == '绿色长寿村导标旗坐标_长寿郊外'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_长寿郊外, True)
                    elif(path == '绿色长寿村导标旗坐标_方寸山'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_方寸山, True)
                    elif(path == '绿色长寿村导标旗坐标_酒店'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_酒店, True)
                    elif(path == '绿色长寿村导标旗坐标_当铺'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_当铺, True)
                    elif(path == '绿色长寿村导标旗坐标_村长家'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_村长家, True)
                    elif(path == '绿色长寿村导标旗坐标_钟书生'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_钟书生, True)
                    elif(path == '绿色长寿村导标旗坐标_孟婆婆'):
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_孟婆婆, True)
                    break
                else:
                    pyautogui.hotkey('alt', 'e')
                    time.sleep(1)
                    if (self.findImgInWindow("all-csqi.png") != None):
                        self.F_选中道具格子(17)
                        navWay = True
                        pydirectinput.click(button="right")
                    else:
                        pyautogui.hotkey('alt', 'e')
                        navWay = False
                    time.sleep(1)

    def F_使用傲来国飞行棋(self, path):
        navWay = True
        desLocation = ""
        if(path == '黄色傲来国导标旗坐标_花果山'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_花果山Str
        elif(path == '黄色傲来国导标旗坐标_女儿村'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_女儿村Str
        elif(path == '黄色傲来国导标旗坐标_东海湾'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_东海湾Str
        elif(path == '黄色傲来国导标旗坐标_布店'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_布店Str
        elif(path == '黄色傲来国导标旗坐标_药店'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_药店Str
        elif(path == '黄色傲来国导标旗坐标_捕鱼人'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_捕鱼人Str
        elif(path == '黄色傲来国导标旗坐标_兵器店'):
            desLocation = pointUtil.黄色傲来国导标旗坐标_兵器店Str
        while(True):
            curLocation = self.获取当前坐标()
            if(desLocation in curLocation):
                break
            else:
                time.sleep(0.5)
                if (navWay and self.findImgInWindow("all-feixing-al.png") != None):
                    if(path == '黄色傲来国导标旗坐标_花果山'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_花果山屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_花果山屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_女儿村'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_女儿村屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_女儿村屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_东海湾'):
                       
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_东海湾屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_东海湾屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_布店'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_布店屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_布店屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_药店'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_药店屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_药店屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_兵器店'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_兵器店屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_兵器店屏幕xy[1])
                    elif(path == '黄色傲来国导标旗坐标_捕鱼人'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.黄色傲来国导标旗坐标_捕鱼人屏幕xy[0], pointUtil.黄色傲来国导标旗坐标_捕鱼人屏幕xy[1])
                    pydirectinput.click()
                    time.sleep(1)
                    pyautogui.hotkey('alt', 'e')
                    break
                elif(navWay == False):
                    self.F_导航到傲来国()
                    if('傲来国飞行符坐标_飞行符' != path):
                        if(path == '黄色傲来国导标旗坐标_花果山'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_花果山)
                        elif(path == '黄色傲来国导标旗坐标_女儿村'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_女儿村)
                        elif(path == '黄色傲来国导标旗坐标_东海湾'):
                            self.F_点击小地图出入口按钮()
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_东海湾)
                            self.F_点击小地图出入口按钮()
                        elif(path == '黄色傲来国导标旗坐标_布店'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_布店)
                        elif(path == '黄色傲来国导标旗坐标_药店'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_药店)
                        elif(path == '黄色傲来国导标旗坐标_兵器店'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_兵器店)
                        elif(path == '黄色傲来国导标旗坐标_捕鱼人'):
                            self.F_小地图寻路器(pointUtil.黄色傲来国导标旗坐标_捕鱼人)
                        break
                else:
                    pyautogui.hotkey('alt', 'e')
                    time.sleep(1)
                    if (self.findImgInWindow("all-alqi.png") != None):
                        self.F_选中道具格子(18)
                        navWay = True
                        pydirectinput.click(button="right")
                    else:
                        pyautogui.hotkey('alt', 'e')
                        navWay = False
                    time.sleep(1)

    def F_导航到大唐国境(self):
        self.F_使用长安城飞行棋('大唐国境出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 25, self.windowArea[1] + 441)
        pydirectinput.click()
        time.sleep(3)

    def F_导航到大唐国境驿站出口(self):
        while True:
            map = self.获取当前地图()
            if map == '大唐国境':
                break
            else:
                self.F_使用长安城飞行棋('长安驿站')
                time.sleep(2)
                self.F_点击驿站老板()
                time.sleep(2)

    def F_导航到地府(self):
        while True:
            map = self.获取当前地图()
            if map == '地府':
                break
            else:
                self.F_导航到大唐国境驿站出口()
                pyautogui.press('tab')
                # 点击地府入口圈圈
                time.sleep(0.5)
                self.F_移动到游戏区域坐标(235, 144)
                pydirectinput.click()
                time.sleep(1)
                pyautogui.press('tab')
                self.F_是否结束寻路()
                pyautogui.press('f9')
                self.F_移动到游戏区域坐标(400, 75)
                pydirectinput.doubleClick()
                time.sleep(1.5)

    def F_点击驿站老板(self):
        pyautogui.press('f9')
        print('开始查找驿站老板')
        yz = None
        while yz is None:
            yz1 = self.findImgInWindow('yz1.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz1 is not None:
                yz = yz1
                break
            yz2 = self.findImgInWindow('yz2.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz2 is not None:
                yz = yz2
                break
            yz3 = self.findImgInWindow('yz3.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz3 is not None:
                yz = yz3
                break
            yz4 = self.findImgInWindow('yz4.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz4 is not None:
                yz = yz4
                break
            time.sleep(0.5)
        if yz is not None:
            print('-找到驿站老板')
            self.pointMove(yz[0], yz[1])
            print('-点击驿站老板')

            pydirectinput.doubleClick()
            time.sleep(1)
            ret = baiduApi.F_大漠红色文字位置识别([self.windowArea[0], self.windowArea[1],
                                        self.windowArea[0] + 600, self.windowArea[1] + 800], '我要去')

            if(ret != None):
                self.pointMove(ret[0], ret[1])
                pydirectinput.click()
        time.sleep(1)

    def F_红色文字位置点击(self, str):
        ret = baiduApi.F_大漠红色文字位置识别([self.windowArea[0], self.windowArea[1],
                                     self.windowArea[0] + 600, self.windowArea[1] + 800], str)

        if(ret != None):
            self.pointMove(ret[0], ret[1])
            pydirectinput.click()
            return True
        else:
            return False

    def F_导航到江南野外(self, 仓库位置='长安城'):
        if(仓库位置 == '建邺城'):
            self.F_导航到建邺城()
            self.F_小地图寻路器([11, 2])
            self.F_移动到游戏区域坐标(272, 449)
            pydirectinput.click()
            time.sleep(1)
            self.F_移动到游戏区域坐标(206, 339)
            pydirectinput.click()
        else:
            self.F_使用长安城飞行棋('江南野外出口')
            time.sleep(1)
            self.pointMove(self.windowArea[0] + 726, self.windowArea[1] + 515)
            pydirectinput.click()
        time.sleep(3)

    def F_导航到狮驼岭(self):
        self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_大唐境外')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 23, self.windowArea[1] + 512)
        pydirectinput.click()
        time.sleep(1)
        time.sleep(2)
        self.pointMove(self.windowArea[0] + 80, self.windowArea[1] + 565)
        pydirectinput.click()
        time.sleep(5)

    def F_导航到大唐境外(self):
        self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_大唐境外')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 23, self.windowArea[1] + 512)
        pydirectinput.click()
        time.sleep(1)

    def F_导航到墨家村(self):
        self.F_导航到大唐境外()
        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 316, self.windowArea[1] + 250)
        pydirectinput.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(38)
        self.pointMove(self.windowArea[0] + 517, self.windowArea[1] + 135)
        pyautogui.press('f9')
        time.sleep(0.5)
        pydirectinput.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 211, self.windowArea[1] + 337)
        pydirectinput.click()
        time.sleep(1)

    def F_导航到麒麟山(self):
        self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_麒麟山')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 35, self.windowArea[1] + 125)
        pydirectinput.click()
        time.sleep(3)

    def F_导航到长寿郊外(self):
        self.F_使用长寿村飞行棋('绿色长寿村导标旗坐标_长寿郊外')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 634, self.windowArea[1] + 518)
        pydirectinput.click()
        time.sleep(4)

    def F_导航到傲来国(self):
        self.F_使用飞行符('傲来国')
        time.sleep(1)

    def F_导航到五庄观(self):
        self.F_导航到大唐国境驿站出口()
        self.F_小地图寻路器([8, 76])
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(40, 222)
        pydirectinput.doubleClick()
        time.sleep(2)
        pyautogui.press('tab')
        self.F_移动到游戏区域坐标(689, 286)
        pydirectinput.doubleClick()
        pyautogui.press('tab')
        self.F_是否结束寻路()
        self.F_移动到游戏区域坐标(680, 222)
        pydirectinput.doubleClick()

    def F_位置分析器(self, 坐标集合, 坐标):
        距离集合 = []
        地点集合 = []
        for key in 坐标集合:
            currentPoint = 坐标集合[key]
            distance = abs(坐标[0] - currentPoint[0]) + \
                abs(坐标[1] - currentPoint[1])
            距离集合.append(distance)
            地点集合.append(key)
        retIndex = 距离集合.index(min(距离集合))
        return 地点集合[retIndex]

    def F_导航到傲来国智能(self, x, y):
        距离集 = []
        for item in pointUtil.傲来点集:
            距离 = abs(x - item[0][0]) + abs(y - item[0][1])
            距离集.append(距离)
        地点 = pointUtil.傲来点集[距离集.index(min(距离集))][1]
        # 坐标 = pointUtil.傲来点集[距离集.index(min(距离集))][0]
        print(地点)
        if(地点 == '傲来国飞行符坐标_飞行符'):
            self.F_导航到傲来国()
        else:
            self.F_使用傲来国飞行棋(地点)
        # self.F_小地图寻路器([x,y])
        time.sleep(1)

    def F_导航到长寿村智能(self, x, y):
        距离集 = []
        for item in pointUtil.长寿村点集:
            距离 = abs(x - item[0][0]) + abs(y - item[0][1])
            距离集.append(距离)
        地点 = pointUtil.长寿村点集[距离集.index(min(距离集))][1]
        # 坐标 = pointUtil.长寿村点集[距离集.index(min(距离集))][0]
        print(地点)
        self.F_使用长寿村飞行棋(地点)
        # self.F_小地图寻路器([x,y])
        time.sleep(1)

    def F_导航到朱紫国智能(self, x, y):
        距离集 = []
        for item in pointUtil.朱紫国点集:
            距离 = abs(x - item[0][0]) + abs(y - item[0][1])
            距离集.append(距离)
        地点 = pointUtil.朱紫国点集[距离集.index(min(距离集))][1]
        print(地点)
        self.F_使用朱紫国飞行棋(地点)
        # self.F_小地图寻路器([x,y])
        time.sleep(1)

    def F_导航到长寿村(self):
        self.F_使用飞行符('长寿村')
        time.sleep(1)

    def F_导航到西梁女国(self):
        self.F_使用飞行符('西梁女国')
        time.sleep(1)

    def F_导航到宝象国(self):
        self.F_使用飞行符('宝象国')
        time.sleep(1)

    def F_导航到建邺城(self):
        self.F_使用飞行符('建邺城')
        time.sleep(1)

    def F_导航到东海湾(self):
        self.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_东海湾')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 221, self.windowArea[1] + 362)
        pydirectinput.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 208, self.windowArea[1] + 336)
        pydirectinput.click()
        time.sleep(1)

    def F_导航到花果山(self):
        self.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_花果山')
        time.sleep(0.5)
        pyautogui.press('f9')
        time.sleep(0.5)
        self.pointMove(self.windowArea[0] + 632, self.windowArea[1] + 103)
        pydirectinput.click()
        time.sleep(4)

    def F_导航到女儿村(self):
        self.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_女儿村')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 50, self.windowArea[1] + 131)
        pydirectinput.click()
        time.sleep(3)

    def F_导航到北俱芦洲(self):
        self.F_导航到长寿郊外()

        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 303, self.windowArea[1] + 344)
        pydirectinput.click()
        time.sleep(26)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 273)
        pydirectinput.doubleClick()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 207, self.windowArea[1] + 340)
        pydirectinput.click()
        time.sleep(1)

    def F_导航到朱紫国(self):
        self.F_使用飞行符('朱紫国')
        time.sleep(1)

    def F_导航到普陀山(self):
        self.F_导航到大唐国境()
        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 416, self.windowArea[1] + 426)
        pydirectinput.click()
        time.sleep(25)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 304)
        pydirectinput.doubleClick()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 206, self.windowArea[1] + 339)
        pydirectinput.click()
        time.sleep(1)

    def F_小地图寻路器(self, 目标坐标, 是否模糊查询=None):
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        self.focusWindow()
        目标坐标x = int(目标坐标[0])
        目标坐标y = int(目标坐标[1])
        isFirstMove = 1
        while True:
            point = self.F_获取小地图寻路坐标()
            print(目标坐标)
            print(point)
            if(point == None or len(point) < 2):
                self.focusWindow()
                continue
            当前坐标x = int(point[0])
            当前坐标y = int(point[1])
            if(是否模糊查询 == None):
                if(目标坐标x == 当前坐标x and 目标坐标y == 当前坐标y):
                    pydirectinput.click()
                    pydirectinput.click()
                    break
                else:
                    # pyautogui.move(目标坐标x - 当前坐标x,  当前坐标y - 目标坐标y)
                    cx = 目标坐标x - 当前坐标x
                    cy = 当前坐标y - 目标坐标y
                    if(isFirstMove < 2):
                        pyautogui.move(cx / 2, cy / 2)
                        isFirstMove = isFirstMove + 1
                    else:
                        if(cx > 20):
                            cx = 20
                        elif(cx < -20):
                            cx = -20
                        if(cy > 10):
                            cy = 10
                        elif(cy < -10):
                            cy = -10
                        pyautogui.move(cx, cy)
                        if(abs(cx) < 20 and abs(cy) < 10):
                            pydirectinput.click()

            else:
                if 目标坐标x - 当前坐标x > 1 or 目标坐标x - 当前坐标x < -1 or 目标坐标y - 当前坐标y > 1 or 目标坐标y - 当前坐标y < -1:
                    cx = 目标坐标x - 当前坐标x
                    cy = 当前坐标y - 目标坐标y
                    if(isFirstMove < 2):
                        pyautogui.move(cx / 2, cy / 2)
                        isFirstMove = isFirstMove + 1
                    else:
                        if(cx > 20):
                            cx = 20
                        elif(cx < -20):
                            cx = -20
                        if(cy > 10):
                            cy = 10
                        elif(cy < -10):
                            cy = -10
                        pyautogui.move(cx, cy)
                        if(abs(cx) < 20 and abs(cy) < 10):
                            pydirectinput.click()
                else:
                    pydirectinput.click()
                    pydirectinput.click()
                    break
        time.sleep(2)
        pyautogui.press('tab')
        self.F_是否结束寻路()

    def F_任务导航器(self, 任务, point):
        if('宝象国' in 任务):
            self.F_导航到宝象国()
        elif('傲来国' in 任务):
            self.F_导航到傲来国智能(int(point[0]), int(point[1]))
        elif('女儿村' in 任务):
            self.F_导航到女儿村()
        elif('建邺城' in 任务):
            self.F_导航到建邺城()
        elif('境外' in 任务):
            self.F_导航到大唐境外()
        elif('普陀山' in 任务):
            self.F_导航到普陀山()
        elif('西梁女国' in 任务):
            self.F_导航到西梁女国()
        elif('江南野外' in 任务):
            self.F_导航到江南野外()
        elif('长寿村' in 任务):
            self.F_导航到长寿村智能(int(point[0]), int(point[1]))
        elif('朱紫国' in 任务):
            self.F_导航到朱紫国智能(int(point[0]), int(point[1]))
        elif('五庄观' in 任务):
            self.F_导航到五庄观()

    def F_移动到游戏区域坐标(self, x, y, 是否战斗操作模式=False, 是否手指操作模式=False):
        self.pointMove(self.windowArea[0] + x,
                       self.windowArea[1] + y, 是否战斗操作模式, 是否手指操作模式)


    当前仓库 = 0
    def F_选择仓库号(self, num):
        if(self.当前仓库 == num):
            return
        self.当前仓库 = num
        if(num == 1):
            self.F_移动到游戏区域坐标(180, 307)
        elif(num == 8):
            self.F_移动到游戏区域坐标(180, 350)
        elif(num == 9):
            self.F_移动到游戏区域坐标(200, 348)
        elif(num == 10):
            self.F_移动到游戏区域坐标(220, 348)
        elif(num == 11):
            self.F_移动到游戏区域坐标(243, 348)
        elif(num == 12):
            self.F_移动到游戏区域坐标(263, 348)
        elif(num == 13):
            self.F_移动到游戏区域坐标(285, 348)
        elif(num == 14):
            self.F_移动到游戏区域坐标(305, 348)
        elif(num == 15):
            self.F_移动到游戏区域坐标(325, 348)
        elif(num == 16):
            self.F_移动到游戏区域坐标(347, 348)
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
        elif(num == 2):
            self.F_移动到游戏区域坐标(202, 312)
        elif(num == 3):
            self.F_移动到游戏区域坐标(225, 312)
        elif(num == 4):
            self.F_移动到游戏区域坐标(245, 312)
        elif(num == 5):
            self.F_移动到游戏区域坐标(269, 312)
        elif(num == 6):
            self.F_移动到游戏区域坐标(289, 312)
        elif(num == 7):
            self.F_移动到游戏区域坐标(309, 312)
        pydirectinput.click()

    def F_回到天台(self):
        while True:
            self.F_选中道具格子(20)
            pydirectinput.click(button="right")
            time.sleep(0.5)
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], 'c08800', '2|-3|b04000,4|-5|400800,5|5|a01800', 0.8, 0)
            if(ret[1] > 0):
                self.pointMove(
                    self.windowArea[0] + 507, self.windowArea[1] + 282)
                time.sleep(0.5)
                pydirectinput.click()
                time.sleep(1.5)
                if(self.获取当前地图() == '长安城'):
                    break
        pyautogui.hotkey('alt', 'e')

    def F_回天台放东西(self, map):
        self.F_选中道具格子(20)
        pydirectinput.click(button="right")
        self.pointMove(self.windowArea[0] + 507, self.windowArea[1] + 282)
        pydirectinput.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        while True:
            point = self.findImgInWindowReturnWindowPoint(
                'all_tiantai_text.png')
            if(point):
                self.F_移动到游戏区域坐标(227, 373)
                pydirectinput.click()
                time.sleep(1)
                break
            else:
                self.F_小地图寻路器([354, 247], True)
                pyautogui.press('f9')
                self.F_移动到游戏区域坐标(286, 333)
                pydirectinput.click()
                pydirectinput.click()
                time.sleep(1)
        num = mapCangkuDict.get(map)
        self.F_选择仓库号(num)
        time.sleep(1)
        # 判断当前仓库是否为空
        for x in range(15):
            if(self.findImgInWindow("all-cangku-gezi.png", 0.9, area= (372, 235, 81, 65)) == None):
                print("仓库已满，寻找空仓库")
                self.切换有空仓库()
            self.F_选中仓库道具格子(x + 1)
            pydirectinput.click(button="right")
            
        self.F_选择仓库号(1)
        time.sleep(1)
        self.F_移动到游戏区域坐标(198, 110)
        pydirectinput.click(button="right")
        time.sleep(1)
        self.F_选中道具格子(1)
        pydirectinput.click(button="right")
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        self.F_选中仓库道具格子(1)
        pydirectinput.click(button="right")
        self.F_移动到游戏区域坐标(720, 35)
        pydirectinput.click(button="right")

    def F_回仓库放东西(self, map, 仓库地点='长安城'):
        self.F_选中道具格子(20)
        pydirectinput.click(button="right")
        if(仓库地点 == '长安城'):
            self.pointMove(self.windowArea[0] + 507, self.windowArea[1] + 282)
            pydirectinput.click()
            time.sleep(1)
            pyautogui.hotkey('alt', 'e')
            time.sleep(1)
            while True:
                point = self.findImgInWindowReturnWindowPoint(
                    'all_tiantai_text.png')
                if(point):
                    self.F_移动到游戏区域坐标(227, 373)
                    pydirectinput.click()
                    time.sleep(1)
                    break
                else:
                    self.F_小地图寻路器([354, 247], True)
                    pyautogui.press('f9')
                    self.F_移动到游戏区域坐标(286, 333)
                    pydirectinput.click()
                    pydirectinput.click()
                    time.sleep(1)
        else:
            self.F_使用飞行符('建邺城')
            time.sleep(1)
            self.F_小地图寻路器([58, 32], True)
            pyautogui.press('f9')
            self.F_移动到游戏区域坐标(315, 275)
            pydirectinput.click()
            pydirectinput.click()
            time.sleep(1)
            self.F_移动到游戏区域坐标(218, 370)
            pydirectinput.click()
            time.sleep(1)
        num = mapCangkuDict.get(map)
        if(num - 5 < 1):
            num = 1
        else:
            num = num - 5
        记录值['满仓库遍历值'] = num
        # 判断当前仓库是否为空
        for x in range(15):
            self.切换有空仓库()
            self.F_选中仓库道具格子(x + 1)
            pydirectinput.click(button="right")
            
        self.F_选择仓库号(1)
        time.sleep(1)
        self.F_移动到游戏区域坐标(198, 110)
        pydirectinput.click(button="right")
        time.sleep(1)
        self.F_选中道具格子(1)
        pydirectinput.click(button="right")
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        self.F_选中仓库道具格子(1)
        pydirectinput.click(button="right")
        self.F_移动到游戏区域坐标(720, 35)
        pydirectinput.click(button="right")

    def 切换有空仓库(self):
        while (记录值['满仓库遍历值'] <= 25):
            print(记录值['满仓库遍历值'])
            self.F_选择仓库号(记录值['满仓库遍历值'])
            time.sleep(0.2)
            if(self.findImgInWindow("all-cangku-gezi.png", confidence=0.99, area=(372, 235, 81, 65)) == None):
                print("不是空仓库")
                记录值['满仓库遍历值'] = 记录值['满仓库遍历值'] + 1
            else:
                print("是空仓库")
                return

    def 获取当前坐标(self):
        ret = baiduApi.F_大漠坐标文字识别([self.windowArea[0], self.windowArea[1],
                                   self.windowArea[0] + 143,  self.windowArea[1] + 47])
        if(ret != None):
            str = ret.replace(",", "")
            return str

    def 获取当前地图(self):
        ret = baiduApi.F_大漠小地图识别([self.windowArea[0], self.windowArea[1],
                                  self.windowArea[0] + 143,  self.windowArea[1] + 47])
        if(ret != None):
            return ret

    def F_获取小地图寻路坐标(self):
        ret = baiduApi.F_大漠小地图寻路坐标识别([self.windowArea[0], self.windowArea[1],
                                      self.windowArea[0] + 800,  self.windowArea[1] + 600])
        if(ret != None):
            ponit = ret.split(',')
            return ponit

    def F_获取任务位置和坐标(self, str):
        map = ""
        if("花果山" in str):
            map = "花果山"
        if("宝象国" in str):
            map = "宝象国"
        elif("五庄观" in str):
            map = "五庄观"
        elif("江南野外" in str):
            map = "江南野外"
        elif("傲来国" in str):
            map = "傲来国"
        elif("墨家村" in str):
            map = "墨家村"
        elif("女儿村" in str):
            map = "女儿村"
        elif("大唐" in str and "外" in str):
            map = "大唐境外"
        elif("大唐国境" in str):
            map = "大唐国境"
        elif("北俱芦洲" in str):
            map = "北俱芦洲"
        elif("驼岭" in str):
            map = "狮驼岭"
        elif("麒麟" in str):
            map = "麒麟山"
        elif("麒山" in str):
            map = "麒麟山"
        elif("东海" in str):
            map = "东海湾"
        elif("建" in str):
            map = "建邺城"
        elif("朱紫国" in str):
            map = "朱紫国"
        elif("普陀山" in str):
            map = "普陀山"
        elif("西梁女国" in str):
            map = "西梁女国"
        elif("宝象国" in str):
            map = "宝象国"
        elif("长寿村" in str):
            map = "长寿村"
        elif("长寿郊外" in str or ("外" in str and "长寿" in str)):
            map = "长寿郊外"
        elif("女国" in str):
            map = "西梁女国"
        else:
            print('未匹配地图', str)

        str = str.replace(".", ",")
        str = str.replace("。", ",")
        str = str.replace("，", ",")
        str1 = re.findall("(\d+,\d+)", str)
        try:
            point = str1[0].split(",")
            return [map, point]
        except:
            return [map, [0, 0]]
            print("An exception occurred")

    def F_打开地图(self):
        while(True):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '001c28', '-7|-5|d8ece0,-3|-8|20c0d0,-7|-5|d8ece0', 0.9, 0)
            if(ret[1] > 0):
                break
            else:
                pyautogui.press('tab')
                time.sleep(2)

    def F_点击自动(self):
        self.F_移动到游戏区域坐标(339, 552)
        pydirectinput.click()

    def F_点击小地图出入口按钮(self):
        pyautogui.press('tab')
        time.sleep(1)
        point = self.findImgInWindowReturnWindowPoint('all_font_intro.png')
        if(point):
            self.F_移动到游戏区域坐标(point[0], point[1])
            pydirectinput.click()
        pyautogui.press('tab')


if __name__ == '__main__':
    window = MHWindow(1, '9')
    window.findMhWindow()
    window.focusWindow()
    time.sleep(1)
    # print(pointUtil.傲来点集[1][0])
    window.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_东海湾')

# window.F_卖装备(15)
# print(window.F_是否结束寻路())
