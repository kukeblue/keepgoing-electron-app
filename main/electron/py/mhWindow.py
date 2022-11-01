# coding=utf-8
import logUtil
import pyautogui
import utils
import baiduApi
import networkApi
import time
import utils
import math
import mouse
import random
import re
import pointUtil
import win32gui
import json


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
    daojuArea = [0, 0, 0, 0]
    daojuArea2 = [0, 0, 0, 0]
    pyHome = __file__.strip('mhWindow.pyc')
    pyImageDir = pyHome + '\config\images'
    gameId = ''
    handle = ''

    def __init__(self, screenUnit):
        print('init')
        self.screenUnit = screenUnit

    def F_获取当前游戏id():
        pyautogui.hotkey('alt', 'e')

    def F_获取设备图片(self, img):
        if('all' in img):
            return '\\' + img
        print('\\' + '9' + '-' + img)
        return '\\' + '9' + '-' + img

    def getTruthPx(self, num):
        return num * self.screenUnit

    def 吃红蓝():
        print('吃红蓝')

    def findMhWindow(self):
        x, y, w, h = self.findPicture('window_top_left_point.png')
        if(x > 0):
            y = y - 12
            x = x - 2
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
            pyautogui.moveTo(
                self.windowArea[0] + 400, self.windowArea[1] + 300)
            # pyautogui.click()
            if(self.gameId == ''):
                data = utils.bindOp()
                self.gameId = data[0]
                self.handle = data[1]

            self.focusWindow()

        else:
            print('未找到前台梦幻窗口')

    def focusWindow(self):
        pyautogui.moveTo(self.windowArea[0] + 400, self.windowArea[1] + 300)
        win32gui.SetForegroundWindow(self.handle)

    def focusWindow2(self):
        pyautogui.moveTo(self.windowArea[0] + 400, self.windowArea[1] + 300)

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
        return pyautogui.locateOnScreen(self.pyImageDir + self.F_获取设备图片(img), confidence=0.7)

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
        point = self.findImgInWindow(img, confidence=confidence, area=area)
        if(point != None):
            point[0] = point[0] - self.windowArea[0]
            point[1] = point[1] - self.windowArea[1]
            return point

    def findImgsInWindow(self, img, confidence=0.95):
        locations = pyautogui.locateAllOnScreen(
            self.pyImageDir + self.F_获取设备图片(img), region=self.windowAreaGui, grayscale=False, confidence=confidence)
        ponits = []
        for location in locations:
            ponits.append([int(location.left / self.screenUnit), int(location.top / self.screenUnit),
                          int(location.width / self.screenUnit), int(location.height / self.screenUnit)])
        return ponits

    def checkpoint(self, 战斗操作模式=False, 手指操作模式=False):
        if(战斗操作模式):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '884448', '4|4|f0ecb8,1|2|401c28,-1|-2|a84048,-4|-3|f0f8f0', 0.6, 0)
            if(ret[1] > 0):
                return (ret[1], ret[2], True)
        if(手指操作模式):
            for x in range(2):
                ret = baiduApi.op.FindMultiColor(
                    self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], 'd86c30', '0|1|d86c30,1|4|c85030,6|-2|200000', 0.5, 0)
                if(ret[1] > 0):
                    return (ret[1], ret[2], True)
        for x in range(3):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '306ca8', '1|0|285490,1|1|285490', 0.95, 0)
            if(ret[1] > 0):
                return (ret[1], ret[2], False)
            ret2 = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], '205890', '0|0|205890', 0.95, 0)
            if(ret2[1] > 0):
                return (ret2[1], ret2[2], False)

    def ClickInWindow(self, x, y):
        self.pointMove(self.windowArea[0] + x, self.windowArea[1] + y)
        utils.click()

    def pointMove(self, x, y, 战斗操作模式=False, 手指操作模式=False, 移动到输入框=False):
        try:
            self.pointMoveNoError(x, y, 战斗操作模式, 手指操作模式, 移动到输入框)
        except Exception as e:
            self.focusWindow()
            pyautogui.click()
            utils.click()
            self.pointMove(x, y, 战斗操作模式=False, 手指操作模式=False, 移动到输入框=False)
        time.sleep(0.3)

    def pointMoveNoError(self, x, y, 战斗操作模式=False, 手指操作模式=False, 移动到输入框=False):
        isFirstMove = 0
        mx = x - 20
        my = y - 16
        safeAreaLeft = self.windowArea2[0] + 100
        safeAreaRight = self.windowArea2[0] + 700
        safeAreaTop = self.windowArea2[1] + 100
        safeAreaBottom = self.windowArea2[1] + 500
        isSafeArea = False
        if(mx > safeAreaLeft and mx < safeAreaRight and my > safeAreaBottom and my < safeAreaTop):
            isSafeArea = True
        finished = False
        lastPoint = None
        循环计数 = 0
        while not finished:
            循环计数 = 循环计数 + 1
            if(循环计数 == 50):
                break
            point = self.checkpoint(战斗操作模式=战斗操作模式, 手指操作模式=手指操作模式)
            if((战斗操作模式 or 移动到输入框 or 手指操作模式) and point == None):
                print('鼠标已经消失')
                point = self.checkpoint(战斗操作模式=战斗操作模式, 手指操作模式=手指操作模式)
                if(point == None):
                    finished = True
                    break
            if(point != None and len(point) > 2 and point[2]):
                finished = True
                return
            if(lastPoint != None and point != None and point[0] == lastPoint[0] and point[1] == lastPoint[1]):
                win32gui.SetForegroundWindow(utils.handle)
                pyautogui.moveTo(
                    self.windowArea[0] + 400, self.windowArea[1] + 300)
                # utils.click()
                time.sleep(1)
                isFirstMove = 0
                continue
            if(point != None):
                dx = point[0] - 48
                dy = point[1] - 38
                if mx - dx > 2 or mx - dx < -2 or my - dy > 2 or my - dy < -2:
                    cx = mx - dx
                    cy = my - dy
                    if(isFirstMove < 2 and isSafeArea == False):
                        utils.move(cx / 2, cy / 2)
                        isFirstMove = isFirstMove + 1
                    else:
                        if(isSafeArea):
                            utils.move(cx, cy)
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
            else:
                self.focusWindow()
                # pyautogui.click()
                isFirstMove = 0
            real = pyautogui.position()
            realX = real[0]
            realY = real[1]
            if(realX > (self.windowArea[0] + 800) or realX < self.windowArea[0] or realY > (self.windowArea[1] + 600) or realY < (self.windowArea[1])):
                win32gui.SetForegroundWindow(utils.handle)
                pyautogui.moveTo(
                    self.windowArea[0] + 400, self.windowArea[1] + 300)
                time.sleep(1)
                isFirstMove = 0

    def F_是否在战斗(self):
        try:
            point = self.findImgInWindow(
                'window_zhandou_mask.png', area=(441, 561, 40, 40))
            if point != None:
                return True
            else:
                if(self.F_识别4小人()):
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

    def 导航到活动人(self):
        self.F_选中道具格子(1)
        utils.click(button="right")
        self.F_移动到游戏区域坐标(357, 327)
        utils.click()
        pyautogui.hotkey('alt', 'e')

    def F_行囊拿红蓝(self, pic):
        num = 18
        if(pic == 'all_hongwan.png'):
            num = 17
        self.F_打开道具()
        self.F_选中道具格子(num)
        time.sleep(1)
        utils.click()
        self.pointMove(
            self.daojuArea[0] + 53, self.daojuArea[1] + 223)
        time.sleep(0.2)
        utils.click()
        time.sleep(0.2)
        utils.click()
        time.sleep(1)
        # 道具拿红
        result = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片(pic), region=self.daojuArea, grayscale=True, confidence=0.75)
        if (result != None):
            self.pointMove(result[0], result[1])
            time.sleep(0.2)
            utils.click()
            time.sleep(0.2)
            self.pointMove(self.daojuArea[0] + 5, self.daojuArea[1] + 224)
            time.sleep(0.2)
            utils.click()
            time.sleep(0.2)
            utils.click()
        else:
            self.pointMove(self.daojuArea[0] + 5, self.daojuArea[1] + 224)
            time.sleep(0.2)
            utils.click()
            return
        # 道具拿红
        time.sleep(1)
        result = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片(pic), region=self.daojuArea, grayscale=True, confidence=0.75)
        if (result != None):
            self.pointMove(result[0], result[1])
            time.sleep(0.2)
            utils.click()
            time.sleep(0.2)
            self.F_选中道具格子(num)
            time.sleep(0.2)
            utils.click()
            time.sleep(0.2)
            utils.rightClick()

    def F_发车检查(self, 是否补蓝=True):
        logUtil.chLog('开始发车')
        self.F_打开道具()
        if (self.findImgInWindow("all-caqi.png") == None):
            networkApi.doUpdateRoleStatus(self.gameId, '补旗')
            while True:
                time.sleep(1)
                result = self.findImgInWindow("all-caqi.png")
                if (result != None):
                    self.pointMove(result[0], result[1])
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    self.F_选中道具格子(16)
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    break
        是否有红 = self.F_吃红()
        是否有蓝 = False
        if(是否补蓝):
            是否有蓝 = self.F_吃蓝()
        if(是否有红 == False):
            print('呼叫补红')
            networkApi.doUpdateRoleStatus(self.gameId, '补红')
            while True:
                time.sleep(1)
                result = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all_hongwan.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
                if (result != None):
                    # 拿到红
                    self.pointMove(result[0], result[1])
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    self.F_选中道具格子(17)
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    utils.rightClick()
                    break
        if(是否补蓝 and 是否有蓝 == False):
            print('呼叫补蓝')
            networkApi.doUpdateRoleStatus(self.gameId, '补蓝')
            while True:
                time.sleep(1)
                result = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all_lanwan.png'), region=self.daojuArea, grayscale=True, confidence=0.85)
                if (result != None):
                    # 拿到蓝
                    self.pointMove(result[0], result[1])
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    self.F_选中道具格子(18)
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.2)
                    utils.rightClick()
                    break

    def F_吃红(self):
        try:
            point = self.findImgInWindow(
                'all-shuidi.png', confidence=0.9, area=(0, 479, 286, 60))
            if point != None:
                self.pointMove(point[0], point[1])
                utils.rightClick()
                return True
            else:
                point = self.findImgInWindow(
                    'all_hongwan.png', area=(0, 469, 296, 80))
                if(point == None):
                    self.F_行囊拿红蓝('all_hongwan.png')
                if point != None:
                    self.pointMove(point[0], point[1])
                    utils.rightClick()
                    return True
                else:
                    return False
        except:
            print('F_吃药 error')

    def F_吃蓝(self):
        try:
            point = self.findImgInWindow(
                'all_lanwan.png', area=(0, 479, 286, 60))
            if(point == None):
                self.F_行囊拿红蓝('all_lanwan.png')
            if point != None:
                self.pointMove(point[0], point[1])
                utils.rightClick()
                return True
            else:
                return False
        except:
            print('F_吃药 error')

    def F_吃药(self):
        try:
            pyautogui.press('f7')
            self.F_吃红()
            self.F_吃蓝()
        except:
            print('F_吃药 error')

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

    def F_识别抓鬼任务(self):
        ret = baiduApi.F_大鬼小鬼任务区间识别([self.windowArea[0] + 640, self.windowArea[1] + 110,
                                    self.windowArea[0] + 640 + 163, self.windowArea[1] + 110 + 233])
        if(ret['鬼王'] != None):
            path = self.F_窗口区域截图('temp_renwu_info.png', ret['鬼王'])
            time.sleep(1)
            text = utils.F_通用文字识别(path)
            ret['鬼王'] = text
        if(ret['捉鬼'] != None):
            path = self.F_窗口区域截图('temp_renwu_info.png', ret['捉鬼'])
            time.sleep(1)
            text = utils.F_通用文字识别(path)
            ret['捉鬼'] = text
        return ret

    def F_识别自定义任务(self):
        位置信息 = [self.windowArea[0] + 342, self.windowArea[1] + 76,
                211, 105]
        # 截图 + ocr识别
        path = self.F_窗口区域截图('temp_zidingyi_renwu_info.png', 位置信息)
        time.sleep(1)
        ret = utils.F_通用文字识别(path)
        return ret

    def F_组队切换验证4小人(self):
        area = [self.windowArea[0] - 3, self.windowArea[1] - 65, 800, 65]
        result = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片(pic), region=area, grayscale=True, confidence=0.75)

    识别4小人次数 = 0

    def F_识别4小人(self):
        ret = baiduApi.F_打图4小人识别([self.windowArea[0], self.windowArea[1],
                                  self.windowArea[0] + 600, self.windowArea[1] + 800])
        if(ret != None):
            x = ret[0]
            y = ret[1]
            位置信息 = [x, y,
                    380, 180]
            print("找到")
            path = self.F_窗口区域截图('temp_4_person_info.png', 位置信息)
            time.sleep(1)
            data = networkApi.getPicPoint(path)
            if(data != '' and "," in data):
                clickPoints = data.split(',')
                if(clickPoints[1]):
                    print('success')
                    self.pointMove(
                        x+int(clickPoints[0]), y+int(clickPoints[1]))
                    time.sleep(0.3)
                    pyautogui.click()
                    utils.click()
                    time.sleep(1)
                    ret = baiduApi.F_打图4小人识别([self.windowArea[0], self.windowArea[1],
                                              self.windowArea[0] + 600, self.windowArea[1] + 800])
                    if(ret == None):
                        return True
                    else:
                        self.F_识别4小人()
                        # return True
            else:
                print('识别失败')
                # raise Exception("识别失败")
        else:
            ret = baiduApi.F_打图4小人识别([self.windowArea[0], self.windowArea[1],
                                      self.windowArea[0] + 600, self.windowArea[1] + 800])
            if(ret != None):
                self.F_识别4小人()
            else:
                print("未找到")

    def F_卖体力(self):
        self.F_小地图寻路器([520, 74])
        time.sleep(1)
        pyautogui.press('f9')
        pyautogui.hotkey('alt', 'h')
        self.F_移动到游戏区域坐标(479, 157)
        utils.click()
        time.sleep(2)
        pyautogui.press('f9')
        pyautogui.hotkey('alt', 'h')
        self.F_移动到游戏区域坐标(374, 153)
        utils.click()
        time.sleep(1.5)
        self.F_移动到游戏区域坐标(219, 340)
        utils.click()
        self.F_移动到游戏区域坐标(431, 295)
        utils.click()
        for i in range(29):
            time.sleep(0.3)
            utils.click()
        self.F_移动到游戏区域坐标(434, 385)
        utils.click()
        time.sleep(0.3)
        utils.rightClick()
        time.sleep(0.3)

    def F_买飞行符(self):
        while True:
            self.F_使用长安城飞行棋('长安驿站')
            time.sleep(1)
            self.F_小地图寻路器([252, 35])
            pyautogui.press('f9')
            pyautogui.hotkey('alt', 'h')
            point = self.findImgInWindow('all-ca-ldr.png', confidence=0.75)
            if(point == None):
                print('继续寻找罗道人')
            else:
                self.pointMove(point[0], point[1])
                utils.click()
                break
        time.sleep(1)
        self.F_移动到游戏区域坐标(174, 340)
        utils.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(403, 204)
        utils.click()
        time.sleep(1)
        for i in range(29):
            utils.click()
        self.F_移动到游戏区域坐标(406, 477)
        utils.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(322, 404)
        utils.click()
        time.sleep(1)
        utils.rightClick()

    def F_买香(self):
        while True:
            self.F_打开道具()
            self.F_使用长安城飞行棋('红色长安城导标旗坐标_杂货店')
            time.sleep(1)
            pyautogui.press('f9')
            pyautogui.hotkey('alt', 'h')
            self.F_移动到游戏区域坐标(472, 194)
            utils.click()
            time.sleep(1)
            pyautogui.press('f9')
            pyautogui.hotkey('alt', 'h')
            self.F_移动到游戏区域坐标(370, 223)
            utils.click()
            time.sleep(1.5)
            point = self.findImgInWindow('all-goumai.png', confidence=0.9)
            if(point != None):
                self.pointMove(point[0] + 3, point[1] + 3)
                time.sleep(0.5)
                break
        utils.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(401, 154)
        utils.click()
        for i in range(29):
            utils.click()
        self.F_移动到游戏区域坐标(406, 477)
        utils.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(322, 404)
        utils.click()
        time.sleep(1)
        utils.rightClick()

    def F_关闭对话(self, 是否多窗口=False):
        time.sleep(0.3)
        point = self.findImgInWindow('all-hysx.png', confidence=0.9)
        if(point != None):
            pyautogui.hotkey('alt', 'f')
        point = self.findImgInWindow('all-close.png', confidence=0.9)
        if(point != None):
            self.pointMove(point[0] + 10, point[1] + 5)
            time.sleep(0.1)
            if(是否多窗口):
                pyautogui.click()
            else:
                utils.click()
            return True
        point = self.findImgInWindow('all-close-feixing.png', confidence=0.9)
        if(point != None):
            self.pointMove(point[0] + 10, point[1] + 5)
            time.sleep(0.1)
            if(是否多窗口):
                pyautogui.click()
            else:
                utils.click()
            return True
        point = self.findImgInWindow('all-close3.png', confidence=0.9)
        if(point != None):
            self.pointMove(point[0] + 10, point[1] + 5)
            time.sleep(0.1)
            if(是否多窗口):
                pyautogui.click()
            else:
                utils.click()
            return True

        # point = self.findImgInWindow('all-kuang.png', confidence=0.95)
        # if(point != None):
        #     self.pointMove(point[0] + 10, point[1] + 10)
        #     utils.rightClick()

    def F_是否结束寻路(self, date=0.5):
        坐标 = self.获取当前坐标()
        self.F_关闭对话()
        count = 0
        while(True):
            if(self.F_是否在战斗()):
                break
            坐标2 = self.获取当前坐标()
            if(坐标2 != None and 坐标 != None and 坐标 == 坐标2):
                if(count > 2):
                    break
                count = count + 1
            else:
                count = 0
                坐标 = 坐标2
            time.sleep(date)

    def F_点击战斗(self, 多次点击=False, 右键点击=False):
        pathMaybe = [[5, 78], [38, 74], [-20, 74], [-10, 74]]
        for i in range(4):
            self.F_移动到游戏区域坐标(574, 442)
            pyautogui.hotkey('alt', 'a')
            utils.rightClick()
            pathMaybeItem = pathMaybe[i]
            point = self.findImgInWindow('all-duibiao.png')
            if(point == None):
                point = baiduApi.F_人物位置识别([self.windowArea[0], self.windowArea[1],
                                           self.windowArea[0] + 800,  self.windowArea[1] + 600])
            if(point != None):
                pyautogui.hotkey('alt', '7')
                utils.rightClick()
                time.sleep(0.5)
                self.pointMove(point[0]+pathMaybeItem[0],
                               point[1] + pathMaybeItem[1])
                time.sleep(0.5)
                if(右键点击 == False):
                    pyautogui.hotkey('alt', 'a')
                    time.sleep(0.1)
                if(多次点击 == True):
                    pyautogui.keyDown('alt')
                    pyautogui.keyDown('a')
                    mouse.double_click()
                    pyautogui.keyUp('a')
                    pyautogui.keyUp('alt')
                else:
                    utils.click()
                time.sleep(1)
                if(self.F_是否在战斗() or 右键点击 == True):
                    break
                else:
                    utils.rightClick()
            time.sleep(0.5)

    def F_自动战斗(self):
        是否战斗 = False
        time.sleep(0.5)
        # self.F_识别4小人()
        是否续自动 = False
        for i in range(4):
            print('F_自动战斗：等待进入战斗:' + str(i))
            time.sleep(0.5)
            if(self.F_是否在战斗()):
                if(是否续自动 == False):
                    是否续自动 = True
                    self.F_点击自动()
                print('F_自动战斗：进入战斗')
                while(True):
                    time.sleep(1)
                    if(self.F_是否结束战斗()):
                        是否战斗 = True
                        print('F_自动战斗：结束战斗')
                        break

    def F_判断人物宝宝低红蓝位(self, 是否吃蓝=True):
        self.F_打开道具()
        pyautogui.press('f7')
        # 检查红
        ret = baiduApi.op.FindMultiColor(
            self.windowArea[0] + 775, self.windowArea[1] + 10, self.windowArea[0] + 775 + 25, self.windowArea[1] + 10 + 7, 'b89090', '2|0|b89090,2|2|885450', 0.75, 0)
        if(ret[1] > 0):
            self.F_吃红()
            print('人物缺红')
        # 检查蓝
        if(是否吃蓝):
            ret = baiduApi.op.FindMultiColor(
                self.windowArea[0] + 748, self.windowArea[1] + 22, self.windowArea[0] + 748 + 25, self.windowArea[1] + 22 + 7, '808080', '2|-1|d0d0d0', 0.8, 0)
            if(ret[1] > 0):
                self.F_吃蓝()
                print('人物缺蓝')
        point = self.findImgInWindow(
            'all-baobao-hong.png', confidence=0.90, area=(650, 0, 20, 20))
        if point != None:
            self.F_移动到游戏区域坐标(620, 100)
            self.F_移动到游戏区域坐标(620, 50)
            self.F_移动到游戏区域坐标(630, 12)
            utils.rightClick()
            print('宝宝缺红')

    def F_判断低蓝位(self):
        # 低蓝位位置 = [self.windowArea[0] + 748, self.windowArea[1] + 22, 15, 7]
        # path = self.F_窗口区域截图('temp_dilan_kedu.png', 低蓝位位置)
        ret = baiduApi.op.FindMultiColor(
            self.windowArea[0] + 748, self.windowArea[1] + 22, self.windowArea[0] + 748 + 15, self.windowArea[1] + 22 + 7, '808080', '2|-1|d0d0d0', 0.8, 0)
        if(ret[1] > 0):
            print('缺蓝')
            self.F_使用酒肆和打坐()

    def F_自动战斗抓律法(self):
        抓次数 = 0
        是否战斗 = False
        time.sleep(0.5)
        self.F_识别4小人()
        for i in range(4):
            print('F_自动战斗：等待进入战斗:' + str(i))
            time.sleep(0.5)
            if(self.F_是否在战斗()):
                self.focusWindow()
                print('F_自动战斗：进入战斗')
                while(True):
                    self.focusWindow()
                    utils.rightClick()
                    time.sleep(1)
                    if(self.F_是否战斗操作()):
                        time.sleep(1)
                        points = self.findImgsInWindow('all-lvfa.png', 0.65)
                        points2 = self.findImgsInWindow('all-linfu.png', 0.98)
                        if(len(points) > 1):
                            points.extend(points2)
                        if(len(points) == 1 and 抓次数 < 6):
                            point = points[0]
                            if(point != None):
                                抓次数 = 抓次数 + 1
                                pyautogui.moveTo(point[0]+15, point[1]+10)
                                self.pointMove(point[0]+15, point[1]+10, True)
                                pyautogui.hotkey('alt', 'g')
                                utils.click()
                        elif(len(points) > 0 and 抓次数 < 6):
                            i = random.randrange(0, len(points), 1)
                            print(i)
                            point = points[i]
                            if(point != None):
                                抓次数 = 抓次数 + 1
                                pyautogui.moveTo(point[0]+15, point[1]+10)
                                self.pointMove(point[0]+15, point[1]+10, True)
                                pyautogui.hotkey('alt', 'g')
                                utils.click()
                        else:
                            self.F_移动到游戏区域坐标(699, 431)
                            utils.click()
                    if(self.F_是否结束战斗()):
                        是否战斗 = True
                        print('F_自动战斗：结束战斗')
                        break

        if(是否战斗):
            pyautogui.press('f7')
            self.F_判断低蓝位()

    def F_自动战斗2(self):
        finish = False
        time.sleep(0.5)
        self.F_识别4小人()
        while(finish == False):
            time.sleep(1)
            if(self.F_是否在战斗()):

                while(True):
                    print('进入战斗')
                    time.sleep(1)
                    if(self.F_是否结束战斗()):
                        finish = True
                        break

    def F_抓鬼自动战斗(self):
        finish = False
        while(finish == False):
            time.sleep(1)
            if(self.F_是否在战斗()):
                time.sleep(2)
                for x in range(5):
                    self.F_识别4小人()
                    self.F_关闭对话(是否多窗口=True)
                    self.F_点击自动2()
                    pyautogui.hotkey('ctrl', 'tab')
                # pyautogui.hotkey('ctrl', 'tab')
                while(True):
                    print('进入战斗')
                    time.sleep(1)
                    if(self.F_是否结束战斗()):
                        finish = True
                        break

    def F_导航到女娲神迹(self):
        point = self.findImgInWindow('all-map-nvsj.png')
        if(point != None):
            return
        self.F_导航到北俱芦洲()
        self.F_小地图寻路器([21, 153], None)
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(264, 196)
        utils.click()
        self.F_移动到游戏区域坐标(199, 354)
        utils.click()
        time.sleep(3)

    def F_导航到天宫(self):
        self.F_导航到长寿郊外()
        self.F_小地图寻路器([28, 59], None)
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(261, 286)
        utils.click()
        self.F_移动到游戏区域坐标(207, 339)
        utils.click()
        time.sleep(1)

    def F_打开道具(self):
        self.focusWindow()
        while True:
            point = self.findImgInWindow('daoju_top.png')
            if(point == None):
                pyautogui.hotkey('alt', 'e')
                time.sleep(0.5)
            else:
                self.daojuArea = [point[0] + 3, point[1] + 50, 250, 205]
                self.daojuArea2 = [point[0] + 3, point[1] +
                                   50, point[0] + 3 + 250, point[1] + 50 + 205]
                break

    def F_关闭道具(self):
        self.focusWindow()
        while True:
            point = self.findImgInWindow('daoju_top.png')
            if(point == None):
                break
            else:
                pyautogui.hotkey('alt', 'e')
                time.sleep(0.5)
                break

    def F_选中道具格子(self, num):
        self.F_打开道具()
        self.focusWindow()
        while True:
            point = self.findImgInWindow('daoju_top.png')
            if(point == None):
                pyautogui.hotkey('alt', 'e')
                time.sleep(0.5)
            else:
                break
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
        firstBlockX = self.windowArea[0] + 453
        firstBlockY = self.windowArea[1] + 248
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)

    def F_选中收购商格子(self, num):
        firstBlockX = self.windowArea[0] + 306
        firstBlockY = self.windowArea[1] + 178
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)

    def F_选中给予格子(self, num):
        firstBlockX = self.windowArea[0] + 299
        firstBlockY = self.windowArea[1] + 139
        left = ((num-1) % 5) * 50
        height = math.floor((num-1) / 5) * 50
        self.pointMove(firstBlockX + left, firstBlockY + height)

    def 丢垃圾铁(self):
        self.F_打开道具()
        self.focusWindow()
        points = self.findImgsInWindow('all-daoju-tie.png')
        print(points)
        for point in points:
            self.pointMove(point[0], point[1])
            time.sleep(0.2)
            if(point != None):
                宝图位置信息 = [self.windowArea[0], self.windowArea[1],
                          self.windowArea[0] + 600, self.windowArea[1] + 600]
                ret = baiduApi.F_查找等级(宝图位置信息)
                if(ret != '' and ret != None and int(ret) < 50):
                    utils.click()
                    self.F_移动到游戏区域坐标(562, 417)
                    utils.click()
                    self.F_移动到游戏区域坐标(351, 342)
                    utils.click()

    def 丢垃圾书(self):
        self.F_打开道具()
        points = self.findImgsInWindow('all-daoju-shu.png')
        for point in points:
            self.pointMove(point[0], point[1])
            time.sleep(0.2)
            if(point != None):
                宝图位置信息 = [self.windowArea[0], self.windowArea[1],
                          self.windowArea[0] + 600, self.windowArea[1] + 600]
                ret = baiduApi.F_查找等级(宝图位置信息)
                if(ret != '' and ret != None and int(ret) < 60):
                    utils.click()
                    self.F_移动到游戏区域坐标(562, 417)
                    utils.click()
                    self.F_移动到游戏区域坐标(351, 342)
                    utils.click()
                    if(int(ret) == 50):
                        time.sleep(1)
                        utils.click()

    def 统计扫货(self):
        point = self.findImgInWindow('all-tie-big.png',  0.85, [self.windowArea[0] + 80, self.windowArea[1],
                                                                550, 480])
        if(point != None):
            ret = baiduApi.F_查找等级([self.windowArea[0], self.windowArea[1],
                                   self.windowArea[0] + 600,  self.windowArea[1] + 800])
            level = int(ret)
            if(level == 50):
                return '50铁'
            elif(level == 60):
                return '60铁'
            elif(level == 70):
                return '70铁'
        point = self.findImgInWindow('all-shu-big.png',  0.85, [self.windowArea[0] + 80, self.windowArea[1],
                                                                520, 480])
        if(point != None):
            ret = baiduApi.F_查找等级([self.windowArea[0], self.windowArea[1],
                                   self.windowArea[0] + 600,  self.windowArea[1] + 800])
            level = int(ret)
            if(level == 50):
                return '50书'
            elif(level == 60):
                return '60书'
            elif(level == 70):
                return '70书'
        point = self.findImgInWindow('all-baotu-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                  520, 480])
        if(point != None):
            return '宝图'
        ret = baiduApi.F_查找等级([self.windowArea[0], self.windowArea[1],
                               self.windowArea[0] + 600,  self.windowArea[1] + 800])
        if(ret != '' and ret != None and int(ret) < 10):
            红玛瑙 = self.findImgInWindow('all-baoshi-malao-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                           520, 480])
            if(红玛瑙 != None):
                return '红玛瑙' + ret
            舍利子 = self.findImgInWindow('all-shelizi-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                      520, 480])
            if(舍利子 != None):
                return '舍利子' + ret
            黑宝石 = self.findImgInWindow('all-heibaoshi-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                        520, 480])
            if(黑宝石 != None):
                return '黑宝石' + ret
            光芒石 = self.findImgInWindow('all-guanmanshi-big.png',  0.95, [self.windowArea[0] + 80, self.windowArea[1],
                                                                         520, 480])
            if(光芒石 != None):
                return '光芒石' + ret
            月亮石 = self.findImgInWindow('all-yueliangshi-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                          520, 480])
            if(月亮石 != None):
                return '月亮石' + ret
            太阳石 = self.findImgInWindow('all-taiyangshi-big.png',  0.75, [self.windowArea[0] + 80, self.windowArea[1],
                                                                         520, 480])
            if(太阳石 != None):
                return '太阳石' + ret
            return '垃圾宝石'

        if(ret != '' and ret != None and int(ret) > 40):
            if(int(ret) == 50):
                return '50环'
            if(int(ret) == 60):
                return '60环'
            if(int(ret) == 70):
                return '70环'

        point = self.findImgInWindow('all-neidang-big.png',  0.85, [self.windowArea[0] + 80, self.windowArea[1],
                                                                    520, 480])
        if(point != None):
            return '内丹'
        point = self.findImgInWindow('all-shoujue-big.png',  0.7, [self.windowArea[0], self.windowArea[1],
                                                                   600, 480])
        if(point != None):
            return '兽决'
        point = self.findImgInWindow('all-66-big.png',  0.78, [self.windowArea[0] + 80, self.windowArea[1],
                                                               520, 480])
        if(point != None):
            return '金柳露'
        point = self.findImgInWindow('all-dinghunzhu-big.png',  0.80, [self.windowArea[0] + 80, self.windowArea[1],
                                                                       520, 480])
        if(point != None):
            return '定魂珠'
        point = self.findImgInWindow('all-jinggangshi-big.png',  0.95, [self.windowArea[0] + 80, self.windowArea[1],
                                                                        520, 480])
        if(point != None):
            return '金刚石'
        point = self.findImgInWindow('all-bishui-big.png',  0.95, [self.windowArea[0] + 80, self.windowArea[1],
                                                                   520, 480])
        if(point != None):
            return '避水珠'
        point = self.findImgInWindow('all-longlin-big.png',  0.95, [self.windowArea[0] + 80, self.windowArea[1],
                                                                    520, 480])
        if(point != None):
            return '龙鳞'
        point = self.findImgInWindow('all-yeguang-big.png',  0.85, [self.windowArea[0] + 80, self.windowArea[1],
                                                                    520, 480])
        if(point != None):
            return '夜光珠'
        return '未知'

    def F_给与东西(self, 接货id, 是否上报收益=True):
        self.F_打开好友信息页面(str(接货id))
        self.F_移动到游戏区域坐标(530, 438)
        time.sleep(0.2)
        utils.click()
        utils.click()
        time.sleep(0.1)
        self.F_移动到游戏区域坐标(513, 489)
        point = self.findImgInWindow('all-geiyu-top.png')
        有货格子 = []
        if(point != None):
            print(point)
            给东西区域top = [point[0]+8, point[1] + 28]
            给东西区域 = [给东西区域top[0], 给东西区域top[1], 252, 200]
            # path = self.F_窗口区域截图('temp_give_area.png', 给东西区域)
            time.sleep(1)
            for i in range(15):
                left = (i % 5) * 50
                height = int(i / 5) * 50
                blockArea = (给东西区域top[0] + left, 给东西区域top[1] + height, 50, 50)
                point2 = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all-give-empty-' + str(i) + '.png'), region=[blockArea[0] - 10, blockArea[1] - 10, blockArea[2] + 10, blockArea[3] + 10], grayscale=True, confidence=0.95)
                if(point2 == None):
                    print('第' + str(i + 1) + '个格子有货')
                    有货格子.append(blockArea)
                # else:
                    # print(point2)
        else:
            print('没找到')
        print('有货格子数量')
        print(len(有货格子))
        if(len(有货格子) == 0):
            self.F_移动到游戏区域坐标(407, 439)
            utils.rightClick()
            time.sleep(1)
            utils.rightClick()
            time.sleep(0.5)
            pyautogui.hotkey('alt', 'f')
            if(是否上报收益 == True):
                networkApi.sendWatuProfit(self.gameId, '')
        networkApi.doUpdateRoleStatus(self.gameId, '空闲')
        if(len(有货格子) > 0):
            print('有货格子循环')
            print(math.ceil(len(有货格子)/3))
            给予次数 = math.ceil(len(有货格子)/3)
            收益 = ''
            给与次数 = math.ceil(len(有货格子)/3)
            for i in range(0, 给与次数):
                for p in range(i * 3, (i + 1) * 3):
                    print(p)
                    if(p < len(有货格子)):
                        item = 有货格子[p]
                        self.F_移动到游戏区域坐标(item[0] - self.windowArea[0] + 25,
                                         item[1] - self.windowArea[1] + 25)

                        ret = self.统计扫货()
                        if(收益 == ''):
                            收益 = ret
                        else:
                            收益 = 收益 + ',' + ret
                        print('识别到：' + ret)
                        utils.click()
                        utils.click()
                        time.sleep(0.2)
                for p in range(i * 3, (i + 1) * 3):
                    if(p < len(有货格子)):
                        item = 有货格子[p]
                        self.F_移动到游戏区域坐标(item[0] - self.windowArea[0] + 25,
                                         item[1] - self.windowArea[1] + 25)
                        time.sleep(0.5)
                        utils.click()
                        utils.click()
                        time.sleep(0.2)
                self.F_移动到游戏区域坐标(405, 497)
                utils.click()
                if(i != (给予次数 - 1)):
                    time.sleep(0.3)
                    self.F_移动到游戏区域坐标(535, 435)
                    time.sleep(0.3)
                    utils.click()
                    pyautogui.click()
                    utils.click()
                else:
                    time.sleep(0.5)
                    self.F_移动到游戏区域坐标(394, 284)
                    utils.rightClick()
                    time.sleep(0.5)
            pyautogui.hotkey('alt', 'f')
            if(是否上报收益 == True):
                networkApi.sendWatuProfit(self.gameId, 收益)
        else:
            networkApi.doUpdateRoleStatus(self.gameId, '空闲')

    def F_卖装备(self):
        self.F_使用飞行符('长安城')
        while True:
            self.F_小地图寻路器([461, 203], None)
            pyautogui.press('f9')
            time.sleep(1)
            self.F_移动到游戏区域坐标(321, 307)
            utils.click()
            time.sleep(1)
            point = self.findImgInWindow('all-zbsg.png')
            if(point != None):
                break
        self.F_移动到游戏区域坐标(174, 337)
        time.sleep(0.5)
        utils.click()
        time.sleep(1)
        有货格子 = []
        point = self.findImgInWindow('all-maizhuanbei-top.png')
        if(point != None):
            print(point)
            卖东西区域top = [point[0]+2, point[1] + 27]
        卖东西区域 = [卖东西区域top[0], 卖东西区域top[1], 250, 200]
        print(卖东西区域top)
        for i in range(20):
            left = (i % 5) * 50
            height = int(i / 5) * 50
            blockArea = (卖东西区域top[0] + left, 卖东西区域top[1] + height, 50, 50)
            # print('第' + str(i + 1) + '个格子')
            # window.F_窗口区域截图('all-daoju-empty-' +
            #                 str(i) + '.png', blockArea)
            point = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片('all-daoju-empty-' + str(i) + '.png'), region=blockArea, grayscale=True, confidence=0.90)
            if(point == None):
                print('第' + str(i + 1) + '个格子有货')
                有货格子.append(blockArea)
        for item in 有货格子:
            self.F_移动到游戏区域坐标(item[0] - self.windowArea[0] + 25,
                             item[1] - self.windowArea[1] + 25)
            utils.click()
            time.sleep(1)
            ret = baiduApi.F_查找等级([self.windowArea[0], self.windowArea[1],
                                   self.windowArea[0] + 600,  self.windowArea[1] + 800])
            print(ret)
            if(ret != '' and ret != None and int(ret) < 50):
                utils.click()
                self.F_移动到游戏区域坐标(404, 440)
                utils.click()
                time.sleep(1)
                self.F_移动到游戏区域坐标(206, 338)
                utils.click()
                time.sleep(1)
                utils.click()

        self.F_移动到游戏区域坐标(510, 398)
        time.sleep(0.5)
        utils.click()
        utils.rightClick()
        time.sleep(0.5)
        pyautogui.press('f9')

    def F_丢垃圾(self, num):
        self.focusWindow()
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        for x in range(num):
            self.F_选中道具格子2(x + 1)
            utils.click()
            pyautogui.moveTo(
                self.windowArea[0] + 450, self.windowArea[1] + 300)
            utils.click()
            time.sleep(0.5)
            self.F_移动到游戏区域坐标(356, 344)
            utils.click()

    def F_判断是否有飞行符(self):
        self.focusWindow()
        self.F_打开道具()
        time.sleep(1)
        result = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片('all-feixing.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
        if (result == None):
            self.pointMove(self.daojuArea[0] + 50, self.daojuArea[1] + 224)
            utils.click()
            time.sleep(1)
            point = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片('all-feixing.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
            if point != None:
                self.pointMove(point[0], point[1])
                utils.click()
                self.pointMove(
                    self.daojuArea[0] + 5, self.daojuArea[1] + 224)
                time.sleep(0.3)
                utils.click()
                utils.click()
                time.sleep(0.1)
                utils.click()
            else:
                self.pointMove(
                    self.daojuArea[0] + 5, self.daojuArea[1] + 224)
                time.sleep(0.3)
                utils.click()
                time.sleep(1)
                self.F_买飞行符()
                self.F_打开道具()
            time.sleep(0.5)
            while True:
                point = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all-feixing.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
                if point != None:
                    self.pointMove(point[0], point[1])
                    utils.click()
                    time.sleep(0.2)
                    self.pointMove(
                        self.daojuArea[0] + 233, self.daojuArea[1] + 176)
                    utils.click()
                    time.sleep(0.2)
                    self.focusWindow()
                    point = pyautogui.locateOnScreen(
                        self.pyImageDir + self.F_获取设备图片('all-feixing.png'), region=[self.daojuArea[0] + 201, self.daojuArea[1] + 160, self.daojuArea[2], self.daojuArea[3]], grayscale=True, confidence=0.75)
                    if(point != None):
                        break
        else:
            return

    def F_使用飞行符(self, path):
        判断飞行符 = False
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
            if(curLocation != '' and curLocation in desLocation):
                break
            else:
                result = self.findImgInWindow("all-wind.png")
                if (result != None):
                    if(path == '傲来国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.傲来国飞行符坐标_屏幕xy[0], pointUtil.傲来国飞行符坐标_屏幕xy[1])
                        utils.click()
                    if(path == '长安城'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.长安城飞行符坐标_屏幕xy[0], pointUtil.长安城飞行符坐标_屏幕xy[1])
                        utils.click()
                    if(path == '朱紫国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.朱紫国飞行符坐标_屏幕xy[0], pointUtil.朱紫国飞行符坐标_屏幕xy[1])
                        utils.click()
                    elif(path == '建邺城'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.建邺城飞行符坐标_屏幕xy[0], pointUtil.建邺城飞行符坐标_屏幕xy[1])
                        utils.click()
                    elif(path == '宝象国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.宝象国飞行符坐标_屏幕xy[0], pointUtil.宝象国飞行符坐标_屏幕xy[1])
                        utils.click()
                    elif(path == '西梁女国'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.西凉女国飞行符坐标_屏幕xy[0], pointUtil.西凉女国飞行符坐标_屏幕xy[1])
                        utils.click()
                    elif(path == '长寿村'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.长寿村飞行符坐标_屏幕xy[0], pointUtil.长寿村飞行符坐标_屏幕xy[1])
                        utils.click()
                    time.sleep(1)
                    break
                else:
                    if(判断飞行符 == False):
                        self.F_判断是否有飞行符()
                        判断飞行符 = True
                    self.F_选中道具格子(20)
                    utils.rightClick()
                    time.sleep(1.5)
        self.F_关闭道具()

    def F_行囊吃香(self):
        是否移动 = False
        while True:
            self.F_打开道具()
            point = pyautogui.locateOnScreen(
                self.pyImageDir + self.F_获取设备图片('all-xiang.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
            if point != None:
                self.pointMove(point[0], point[1])
                time.sleep(0.2)
                if(是否移动 == True):
                    utils.click()
                    time.sleep(0.1)
                    self.F_选中道具格子(19)
                    time.sleep(0.2)
                    utils.click()
                    time.sleep(0.1)
                utils.rightClick()
                time.sleep(0.1)
                break
            else:
                是否移动 = True
                self.pointMove(self.daojuArea[0] + 50, self.daojuArea[1] + 224)
                utils.click()
                time.sleep(1)
                point = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all-xiang.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
                if point != None:
                    self.pointMove(point[0], point[1])
                    utils.click()
                    self.pointMove(
                        self.daojuArea[0] + 5, self.daojuArea[1] + 224)
                    time.sleep(0.3)
                    utils.click()
                    time.sleep(0.3)
                    utils.click()
                    time.sleep(0.5)
                else:
                    self.pointMove(
                        self.daojuArea[0] + 5, self.daojuArea[1] + 224)
                    time.sleep(0.3)
                    utils.click()
                    time.sleep(1)
                    self.F_买香()
                    time.sleep(0.5)
        if(self.F_查看摄妖香分钟() == None):
            self.F_行囊吃香()

    def F_吃香(self):
        self.F_行囊吃香()

    def F_吃香2(self):
        self.F_打开道具()
        point = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片('all-xiang.png'), region=self.daojuArea, grayscale=True, confidence=0.75)
        if(point != None):
            self.pointMove(point[0], point[1])
            utils.rightClick()
            time.sleep(0.1)
        self.F_关闭道具()

    def F_吃动名草(self):
        self.F_打开道具()
        point = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片('all-daoju-dmc.png'), region=self.daojuArea, grayscale=True, confidence=0.85)
        if(point != None):
            self.pointMove(point[0], point[1])
            utils.rightClick()
            time.sleep(0.1)
        self.F_关闭道具()

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
        elif(path == '红色长安城导标旗坐标_酒店'):
            desLocation = pointUtil.红色长安城导标旗坐标_酒店Str
        elif(path == '红色长安城导标旗坐标_商会'):
            desLocation = pointUtil.红色长安城导标旗坐标_商会Str
        elif(path == '红色长安城导标旗坐标_杂货店'):
            desLocation = pointUtil.红色长安城导标旗坐标_杂货店Str
        while(True):
            curLocation = self.获取当前坐标()
            if(desLocation == curLocation):
                break
            else:
                if (navWay):
                    if(path == '大唐国境出口'):
                        self.pointMove(
                            self.windowArea[0] + 139, self.windowArea[1] + 435)
                        utils.click()
                    if(path == '长安驿站'):
                        self.pointMove(
                            self.windowArea[0] + 407, self.windowArea[1] + 398)
                        utils.click()
                    elif(path == '江南野外出口'):
                        self.pointMove(
                            self.windowArea[0] + 657, self.windowArea[1] + 435)
                        utils.click()
                    elif(path == '化生寺出口'):
                        self.pointMove(
                            self.windowArea[0] + 627, self.windowArea[1] + 169)
                        utils.click()
                    elif(path == '红色长安城导标旗坐标_酒店'):
                        self.pointMove(
                            self.windowArea[0] + 583, self.windowArea[1] + 277)
                        utils.click()
                    elif(path == '红色长安城导标旗坐标_商会'):
                        self.pointMove(
                            self.windowArea[0] + 455, self.windowArea[1] + 421)
                        utils.click()
                    elif(path == '红色长安城导标旗坐标_杂货店'):
                        self.pointMove(
                            self.windowArea[0] + 654, self.windowArea[1] + 309)
                        utils.click()
                    time.sleep(0.5)
                    pyautogui.hotkey('alt', 'e')
                    break
                elif(navWay == False):
                    self.F_使用飞行符('长安城')
                    if(path == '大唐国境出口'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_大唐国境, True)
                    elif(path == '长安驿站'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_驿站, True)
                    elif(path == '江南野外出口'):
                        # 关闭出入口
                        self.F_点击小地图出入口按钮()
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_江南野外, None)
                        self.F_点击小地图出入口按钮()
                    elif(path == '化生寺出口'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_化生寺, None)
                    elif(path == '红色长安城导标旗坐标_酒店'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_酒店, None)
                    elif(path == '红色长安城导标旗坐标_商会'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_商会, None)
                    elif(path == '红色长安城导标旗坐标_杂货店'):
                        self.F_小地图寻路器(pointUtil.红色长安城导标旗坐标_杂货店, None)
                    break
                else:
                    self.F_打开道具()
                    time.sleep(0.5)
                    if (self.findImgInWindow("all-caqi.png") != None):
                        navWay = True
                        self.F_选中道具格子(16)
                        utils.rightClick()
                    else:
                        navWay = False
                        self.F_打开道具()
                    time.sleep(0.5)

    def F_使用朱紫国飞行棋(self, path):
        self.F_打开道具()
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
            if(curLocation != '' and desLocation == curLocation):
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
                        utils.click()
                        time.sleep(0.5)
                        self.F_关闭道具()
                    time.sleep(0.3)
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
                    self.F_打开道具()
                    time.sleep(1)
                    if (self.findImgInWindow("all-zzqi.png") != None):
                        self.F_选中道具格子(19)
                        time.sleep(0.2)
                        navWay = True
                        utils.rightClick()
                        time.sleep(0.5)
                    else:
                        navWay = False
                        self.F_打开道具()
                    time.sleep(0.5)

    def F_使用长寿村飞行棋(self, path):
        self.F_打开道具()
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
            if(curLocation != '' and desLocation in curLocation):
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
                    elif(path == '绿色长寿村导标旗坐标_孟婆婆'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_孟婆婆屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_孟婆婆屏幕xy[1])
                    elif(path == '绿色长寿村导标旗坐标_钟书生'):
                        self.F_移动到游戏区域坐标(
                            pointUtil.绿色长寿村导标旗坐标_钟书生屏幕xy[0], pointUtil.绿色长寿村导标旗坐标_钟书生屏幕xy[1])
                    if(path == '长寿村飞行符坐标_飞行符'):
                        self.F_导航到长寿村()
                    else:
                        utils.click()
                        time.sleep(0.5)
                        self.F_关闭道具()
                        break
                elif(navWay == False):
                    self.F_导航到长寿村()
                    time.sleep(1)
                    if(path == '绿色长寿村导标旗坐标_长寿郊外'):
                        self.F_点击小地图出入口按钮()
                        self.F_小地图寻路器(pointUtil.绿色长寿村导标旗坐标_长寿郊外, True)
                        self.F_点击小地图出入口按钮()
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
                    self.F_打开道具()
                    time.sleep(1)
                    if (self.findImgInWindow("all-csqi.png") != None):
                        self.F_选中道具格子(17)
                        navWay = True
                        utils.rightClick()
                    else:
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
            if(curLocation != '' and desLocation in curLocation):
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
                    utils.click()
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
                        utils.rightClick()
                    else:
                        pyautogui.hotkey('alt', 'e')
                        navWay = False
                    time.sleep(1)

    def F_导航到大唐国境(self):
        self.F_使用长安城飞行棋('大唐国境出口')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 25, self.windowArea[1] + 441)
        utils.click()
        time.sleep(1.5)

    def F_导航到酒店门口(self):
        self.F_使用长安城飞行棋('红色长安城导标旗坐标_酒店')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 25, self.windowArea[1] + 441)
        utils.click()
        time.sleep(2)

    def F_导航到大唐国境驿站出口(self):
        while True:
            map = self.获取当前地图()
            if map == '大唐国境':
                break
            else:
                self.F_使用长安城飞行棋('长安驿站')
                time.sleep(1)
                self.F_点击驿站老板()
                time.sleep(0.5)

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
                utils.click()
                time.sleep(1)
                pyautogui.press('tab')
                self.F_是否结束寻路()
                pyautogui.press('f9')
                self.F_移动到游戏区域坐标(400, 75)
                utils.doubleClick()
                time.sleep(1.5)

    def F_点击驿站老板(self):
        pyautogui.press('f9')
        pyautogui.hotkey('alt', 'h')
        print('开始查找驿站老板')
        yz = None
        while yz is None:
            yz1 = self.findImgInWindow(
                'yz1.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz1 is not None:
                yz = yz1
                break
            yz2 = self.findImgInWindow(
                'yz2.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz2 is not None:
                yz = yz2
                break
            yz3 = self.findImgInWindow(
                'yz3.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz3 is not None:
                yz = yz3
                break
            yz4 = self.findImgInWindow(
                'yz4.png', confidence=0.65, area=(303, 54, 379, 197))
            if yz4 is not None:
                yz = yz4
                break
            time.sleep(0.5)
        if yz is not None:
            print('-找到驿站老板')
            self.pointMove(yz[0], yz[1])
            print('-点击驿站老板')

            utils.doubleClick()
            time.sleep(1)
            ret = baiduApi.F_大漠红色文字位置识别([self.windowArea[0], self.windowArea[1],
                                         self.windowArea[0] + 600, self.windowArea[1] + 800], '我要去')

            if(ret != None):
                self.pointMove(ret[0], ret[1])
                utils.click()
        time.sleep(0.5)

    def F_红色文字位置点击(self, str):
        ret = baiduApi.F_大漠红色文字位置识别([self.windowArea[0], self.windowArea[1],
                                     self.windowArea[0] + 600, self.windowArea[1] + 800], str)

        if(ret != None):
            self.pointMove(ret[0], ret[1])
            utils.click()
            return True
        else:
            return False

    def F_导航到江南野外(self, 仓库位置='长安城'):
        if(self.获取当前地图() == '江南野外'):
            return
        if(仓库位置 == '建邺城'):
            self.F_导航到建邺城()
            self.F_小地图寻路器([11, 2])
            self.F_移动到游戏区域坐标(272, 449)
            utils.click()
            time.sleep(1)
            self.F_移动到游戏区域坐标(206, 339)
            utils.click()
            time.sleep(3)
        else:
            while True:
                self.F_使用长安城飞行棋('江南野外出口')
                time.sleep(1)
                self.pointMove(
                    self.windowArea[0] + 726, self.windowArea[1] + 515)
                utils.click()
                time.sleep(3)
                if(self.获取当前地图() == '江南野外'):
                    break

    def F_导航到狮驼岭(self):
        self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_大唐境外')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 40, self.windowArea[1] + 525)
        utils.click()
        time.sleep(1)
        time.sleep(2)
        self.pointMove(self.windowArea[0] + 80, self.windowArea[1] + 565)
        utils.click()
        time.sleep(5)

    def F_导航到大唐境外(self):
        if(self.获取当前地图() == '大唐境外'):
            return
        for i in range(3):
            self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_大唐境外')
            time.sleep(1)
            self.pointMove(self.windowArea[0] + 40, self.windowArea[1] + 525)
            utils.click()
            time.sleep(3)
            if(self.获取当前地图() == '大唐境外'):
                break

    def F_导航到墨家村(self):
        self.F_导航到大唐境外()
        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 316, self.windowArea[1] + 250)
        utils.click()
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(38)
        self.pointMove(self.windowArea[0] + 517, self.windowArea[1] + 135)
        pyautogui.press('f9')
        time.sleep(0.5)
        utils.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 211, self.windowArea[1] + 337)
        utils.click()
        time.sleep(1)

    def F_导航到麒麟山(self):
        self.F_使用朱紫国飞行棋('白色朱紫国导标旗坐标_麒麟山')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 35, self.windowArea[1] + 125)
        utils.click()
        utils.click()
        time.sleep(3)

    def F_导航到碗子山(self):
        self.F_使用飞行符('宝象国')
        self.F_小地图寻路器([150, 6], True)
        self.F_移动到游戏区域坐标(664, 461)
        utils.click()
        time.sleep(2)

    def F_导航到海底迷宫(self):
        self.F_导航到花果山()
        self.F_小地图寻路器([107, 7], True)
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(260, 457)
        utils.click()
        self.F_移动到游戏区域坐标(210, 334)
        utils.click()
        time.sleep(2)

    def F_导航到海底迷宫(self):
        self.F_导航到花果山()
        self.F_小地图寻路器([107, 7], True)
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(260, 457)
        utils.click()
        self.F_移动到游戏区域坐标(210, 334)
        utils.click()
        time.sleep(2)

    def F_导航到地狱迷宫三层(self):
        self.F_导航到地府()
        self.F_小地图寻路器([34, 115])
        self.F_移动到游戏区域坐标(443, 105)
        utils.click()
        time.sleep(1)
        self.F_小地图寻路器([9, 10], None, 30)
        self.F_移动到游戏区域坐标(183, 457)
        utils.click()
        time.sleep(1)
        self.F_小地图寻路器([111, 37], None, 30)
        self.F_移动到游戏区域坐标(734, 272)
        utils.click()
        time.sleep(1)

    def F_导航到长寿郊外(self):
        self.F_使用长寿村飞行棋('绿色长寿村导标旗坐标_长寿郊外')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 634, self.windowArea[1] + 518)
        utils.click()
        time.sleep(4)

    def F_导航到傲来国(self):
        self.F_使用飞行符('傲来国')
        time.sleep(1)

    def F_导航到五庄观(self):
        self.F_导航到大唐国境()
        self.F_小地图寻路器([8, 76], True)
        pyautogui.press('f9')
        self.F_移动到游戏区域坐标(40, 222)
        utils.doubleClick()
        time.sleep(2)
        pyautogui.press('tab')
        self.F_移动到游戏区域坐标(686, 284)
        time.sleep(0.2)
        utils.doubleClick()
        pyautogui.press('tab')
        self.F_是否结束寻路()
        self.F_移动到游戏区域坐标(680, 222)
        utils.doubleClick()
        time.sleep(3)

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
        utils.click()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 208, self.windowArea[1] + 336)
        utils.click()
        time.sleep(1)

    def F_导航到化生寺(self):
        self.F_使用长安城飞行棋('化生寺出口')
        time.sleep(0.5)
        pyautogui.press('f9')
        time.sleep(0.5)
        self.pointMove(self.windowArea[0] + 479, self.windowArea[1] + 63)
        utils.click()
        time.sleep(3)

    def F_导航到花果山(self):
        if(self.获取当前地图() == '花果山'):
            return
        for i in range(3):
            self.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_花果山')
            time.sleep(1)
            pyautogui.press('f9')
            pyautogui.hotkey('alt', 'h')
            time.sleep(1)
            self.pointMove(self.windowArea[0] + 632, self.windowArea[1] + 103)
            self.pointMove(self.windowArea[0] + 723, self.windowArea[1] + 84)
            utils.click()
            time.sleep(3)
            if(self.获取当前地图() == '花果山'):
                break

    def F_导航到女儿村(self):
        self.F_使用傲来国飞行棋('黄色傲来国导标旗坐标_女儿村')
        time.sleep(1)
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 50, self.windowArea[1] + 131)
        utils.click()
        time.sleep(3)

    def F_导航到北俱芦洲(self):
        self.F_导航到长寿郊外()

        pyautogui.press('tab')
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 303, self.windowArea[1] + 344)
        utils.click()
        time.sleep(26)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 273)
        utils.doubleClick()
        time.sleep(1)
        self.pointMove(self.windowArea[0] + 207, self.windowArea[1] + 340)
        utils.click()
        time.sleep(1)

    def F_导航到朱紫国(self):
        self.F_使用飞行符('朱紫国')
        time.sleep(1)

    def F_集体酒肆(self):
        pyautogui.press('f6')
        time.sleep(1)
        if(self.findImgInWindow("all-woyaoxiuxi.png", 0.9, area=(151, 381, 81, 35)) != None):
            print("我要休息")
            self.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
            self.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
            self.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            self.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            self.F_移动到游戏区域坐标(190, 394)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(2)

    def F_使用酒肆和打坐(self):
        pyautogui.press('f7')
        pyautogui.press('f6')
        time.sleep(1)
        if(self.findImgInWindow("all-woyaoxiuxi.png", 0.70, area=(146, 378, 100, 60)) != None):
            print("我要休息")
            self.F_移动到游戏区域坐标(190, 394)
            time.sleep(0.5)
            utils.click()

    def F_导航到普陀山(self):
        self.F_导航到大唐国境()
        pyautogui.press('tab')
        self.pointMove(self.windowArea[0] + 416, self.windowArea[1] + 426)
        utils.click()
        time.sleep(23)
        pyautogui.press('tab')
        pyautogui.press('f9')
        self.pointMove(self.windowArea[0] + 402, self.windowArea[1] + 304)
        utils.doubleClick()
        time.sleep(0.5)
        self.pointMove(self.windowArea[0] + 206, self.windowArea[1] + 339)
        utils.click()
        time.sleep(0.5)

    def F_小地图寻路器(self, 目标坐标, 是否模糊查询=None, 等到时间=0, openTab=False):
        time.sleep(0.5)
        if(openTab == False):
            pyautogui.press('tab')
        time.sleep(0.5)
        目标坐标x = int(目标坐标[0])
        目标坐标y = int(目标坐标[1])
        isFirstMove = 1
        错误次数 = 0
        循环次数 = 0
        while True:
            循环次数 = 循环次数 + 1
            if(循环次数 > 30):
                break
            point = self.F_获取小地图寻路坐标()
            print(目标坐标)
            print(point)
            if(point == None or len(point) < 2):
                错误次数 = 错误次数 + 1
                self.focusWindow()
                if(错误次数 == 5):
                    break
                continue
            当前坐标x = 0
            当前坐标y = 0
            try:
                当前坐标x = int(point[0])
                当前坐标y = int(point[1])
            except:
                continue
            if(是否模糊查询 == None):
                if(目标坐标x == 当前坐标x and 目标坐标y == 当前坐标y):
                    utils.click()
                    utils.click()
                    break
                else:
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
                            utils.click()

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
                            utils.click()
                else:
                    utils.click()
                    utils.click()
                    break
        time.sleep(2)
        pyautogui.press('tab')
        if(等到时间 == 0):
            self.F_是否结束寻路()
        else:
            time.sleep(等到时间)

    def F_打开好友信息页面(self, id):
        self.F_移动到游戏区域坐标(600, 140)
        self.F_移动到游戏区域坐标(682, 76)
        while True:
            pyautogui.hotkey('alt', 'f')
            time.sleep(0.5)
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0] + 530, self.windowArea2[1] + 111, self.windowArea2[1] + 530 + 85, self.windowArea2[1] + 111 + 65, '380808', '1|3|b05c48,3|0|b86850', 0.95, 0)
            if(ret[1] > 0):
                self.F_移动到游戏区域坐标(567, 139)
                utils.click()
                self.F_移动到游戏区域坐标(682, 76)
            else:
                pyautogui.hotkey('alt', 'f')
                break
        self.F_移动到游戏区域坐标(682, 76)
        pyautogui.hotkey('alt', 'f')
        time.sleep(0.5)
        utils.doubleClick()
        time.sleep(1)
        for x in range(15):
            pyautogui.press('left')
            time.sleep(0.1)
            pyautogui.press('delete')
        pyautogui.write(id)
        time.sleep(1)
        self.focusWindow()
        self.F_移动到游戏区域坐标(657, 133)
        time.sleep(0.5)
        ret = baiduApi.op.CmpColor(
            self.windowArea2[0] + 750, self.windowArea2[1] + 140, 'dcda71-000000', 0.8)
        print(ret)
        if(ret == 1):
            time.sleep(0.2)
            utils.rightClick()
            utils.rightClick()
            time.sleep(0.3)
        else:
            self.F_移动到游戏区域坐标(628, 466)
            self.F_移动到游戏区域坐标(650, 565, True)
            utils.click()
            pyautogui.press('tab')
            self.F_移动到游戏区域坐标(469, 231)
            pyautogui.press('tab')
            time.sleep(0.5)
            utils.doubleClick()
            for x in range(15):
                pyautogui.press('left')
                time.sleep(0.1)
                pyautogui.press('delete')
            pyautogui.write(id)
            self.focusWindow()
            self.F_移动到游戏区域坐标(544, 233)
            utils.click()
            self.F_移动到游戏区域坐标(363, 409)
            utils.click()
            time.sleep(1)
            # self.focusWindow()
            self.F_移动到游戏区域坐标(453, 201)
            time.sleep(0.3)
            utils.rightClick()
            time.sleep(1)
            pyautogui.hotkey('alt', 'f')
            self.F_打开好友信息页面(id)

    def 医宝宝(self):
        # self.F_使用飞行符('朱紫国')
        self.F_小地图寻路器([100, 57])
        pyautogui.press('f9')
        pyautogui.hotkey('alt', 'h')
        self.F_移动到游戏区域坐标(488, 309)
        utils.click()
        time.sleep(1)
        self.F_移动到游戏区域坐标(295, 400)
        time.sleep(0.5)
        utils.click()
        time.sleep(0.5)
        self.F_关闭对话()

    def F_任务导航器(self, 任务, point):
        self.focusWindow()
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
        elif('西梁女国' in 任务 or '女国' in 任务):
            self.F_导航到西梁女国()
        elif('江南野外' in 任务 or '野外' in 任务):
            self.F_导航到江南野外()
        elif('长寿村' in 任务):
            self.F_导航到长寿村智能(int(point[0]), int(point[1]))
        elif('朱紫国' in 任务):
            self.F_导航到朱紫国智能(int(point[0]), int(point[1]))
        elif('五庄观' in 任务):
            self.F_导航到五庄观()
        elif('北俱芦洲' in 任务):
            self.F_导航到北俱芦洲()
        elif('狮驼岭' in 任务):
            self.F_导航到狮驼岭()
        elif('花果山' in 任务):
            self.F_导航到花果山()
        elif('长寿郊外' in 任务):
            self.F_导航到长寿郊外()
        elif('东海湾' in 任务):
            self.F_导航到东海湾()
        elif('化生寺' in 任务):
            self.F_导航到化生寺()
        elif('地府' in 任务):
            self.F_导航到地府()
        elif('海底迷宫' in 任务):
            self.F_导航到海底迷宫()
        elif('碗子山' in 任务):
            self.F_导航到碗子山()
        elif('地狱迷宫' in 任务):
            self.F_导航到地狱迷宫三层()
        elif('大唐国境' in 任务):
            self.F_导航到大唐国境()
        elif('麒麟山' in 任务):
            self.F_导航到麒麟山()
        elif('女娲神迹' in 任务):
            self.F_导航到女娲神迹()
        elif('天宫' in 任务):
            self.F_导航到天宫()
        else:
            logUtil.chLog('未匹配到地图：' + 任务)

    def F_移动到游戏区域坐标(self, x, y, 是否战斗操作模式=False, 是否手指操作模式=False, 移动到输入框=False):
        self.pointMove(self.windowArea[0] + x,
                       self.windowArea[1] + y, 是否战斗操作模式, 是否手指操作模式, 移动到输入框)

    当前仓库 = 0

    def F_选择仓库号(self, num):
        if(self.当前仓库 == num):
            return
        self.当前仓库 = num
        if(num == 1):
            self.F_移动到游戏区域坐标(131, 441)
        elif(num == 8):
            self.F_移动到游戏区域坐标(131, 483)
        elif(num == 9):
            self.F_移动到游戏区域坐标(152, 484)
        elif(num == 10):
            self.F_移动到游戏区域坐标(174, 483)
        elif(num == 11):
            self.F_移动到游戏区域坐标(195, 482)
        elif(num == 12):
            self.F_移动到游戏区域坐标(216, 482)
        elif(num == 13):
            self.F_移动到游戏区域坐标(236, 482)
        elif(num == 14):
            self.F_移动到游戏区域坐标(256, 482)
        elif(num == 15):
            self.F_移动到游戏区域坐标(276, 482)
        elif(num == 16):
            self.F_移动到游戏区域坐标(296, 482)
        elif(num == 17):
            self.F_移动到游戏区域坐标(130, 506)
        elif(num == 18):
            self.F_移动到游戏区域坐标(154, 510)
        elif(num == 19):
            self.F_移动到游戏区域坐标(175, 510)
        elif(num == 20):
            self.F_移动到游戏区域坐标(194, 507)
        elif(num == 21):
            self.F_移动到游戏区域坐标(215, 507)
        elif(num == 22):
            self.F_移动到游戏区域坐标(235, 507)
        elif(num == 23):
            self.F_移动到游戏区域坐标(255, 507)
        elif(num == 24):
            self.F_移动到游戏区域坐标(275, 507)
        elif(num == 25):
            self.F_移动到游戏区域坐标(299, 507)
        elif(num == 2):
            self.F_移动到游戏区域坐标(152, 436)
        elif(num == 3):
            self.F_移动到游戏区域坐标(172, 436)
        elif(num == 4):
            self.F_移动到游戏区域坐标(192, 436)
        elif(num == 5):
            self.F_移动到游戏区域坐标(212, 436)
        elif(num == 6):
            self.F_移动到游戏区域坐标(232, 436)
        elif(num == 7):
            self.F_移动到游戏区域坐标(252, 436)
        utils.click()

    def F_回到天台(self):
        while True:
            self.F_选中道具格子(20)
            utils.rightClick()
            time.sleep(0.5)
            ret = baiduApi.op.FindMultiColor(
                self.windowArea2[0], self.windowArea2[1], self.windowArea2[2], self.windowArea2[3], 'c08800', '2|-3|b04000,4|-5|400800,5|5|a01800', 0.8, 0)
            if(ret[1] > 0):
                self.pointMove(
                    self.windowArea[0] + 507, self.windowArea[1] + 282)
                time.sleep(0.5)
                utils.click()
                time.sleep(1.5)
                if(self.获取当前地图() == '长安城'):
                    break
        pyautogui.hotkey('alt', 'e')

    def F_回天台放东西(self, map):
        self.F_选中道具格子(20)
        utils.rightClick()
        self.pointMove(self.windowArea[0] + 507, self.windowArea[1] + 282)
        utils.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'e')
        time.sleep(1)
        while True:
            point = self.findImgInWindowReturnWindowPoint(
                'all_tiantai_text.png')
            if(point):
                self.F_移动到游戏区域坐标(227, 373)
                utils.click()
                time.sleep(1)
                break
            else:
                self.F_小地图寻路器([354, 247], True)
                pyautogui.press('f9')
                pyautogui.hotkey('alt', 'h')
                self.F_移动到游戏区域坐标(286, 333)
                utils.click()
                utils.click()
                time.sleep(1)
        num = mapCangkuDict.get(map)
        self.F_选择仓库号(num)
        time.sleep(1)
        # 判断当前仓库是否为空
        for x in range(15):
            if(self.findImgInWindow("all-cangku-gezi.png", 0.9, area=(323, 370, 49, 49)) == None):
                print("仓库已满，寻找空仓库")
                self.切换有空仓库()
            self.F_选中仓库道具格子(x + 1)
            utils.rightClick()

        self.F_选择仓库号(1)
        time.sleep(1)
        self.F_移动到游戏区域坐标(144, 240)
        utils.rightClick()
        time.sleep(1)
        self.F_选中道具格子(1)
        utils.rightClick()
        time.sleep(1)
        self.F_选中仓库道具格子(1)
        utils.rightClick()
        self.F_移动到游戏区域坐标(689, 142)
        utils.click()
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'e')
        self.F_移动到游戏区域坐标(720, 35)
        utils.rightClick()

    def F_回仓库丢小号(self, 接货id, 仓库地点='长安城'):
        self.F_卖装备()
        self.丢垃圾书()
        self.丢垃圾铁()
        if(仓库地点 == '长安城'):
            self.F_使用飞行符('长安城')
            time.sleep(1)
            pyautogui.hotkey('alt', 'e')
            time.sleep(1)
            while True:
                point = self.findImgInWindowReturnWindowPoint(
                    'all_tiantai_text.png')
                if(point):
                    self.F_移动到游戏区域坐标(227, 373)
                    utils.click()
                    time.sleep(1)
                    break
                else:
                    self.F_小地图寻路器([354, 247], True)
                    pyautogui.press('f9')
                    pyautogui.hotkey('alt', 'h')
                    self.F_移动到游戏区域坐标(286, 333)
                    utils.click()
                    utils.click()
                    time.sleep(1)
        else:
            self.F_使用飞行符('建邺城')
            pyautogui.press('f9')
            time.sleep(0.5)
            pyautogui.hotkey('alt', 'h')
            time.sleep(0.5)
        logUtil.chLog('接货id:' + str(接货id))
        self.F_给与东西(接货id)

    def F_回仓库放东西(self, map, 仓库地点='长安城'):

        if(仓库地点 == '长安城'):
            self.F_使用飞行符('长安城')
            time.sleep(1)
            while True:
                point = self.findImgInWindowReturnWindowPoint(
                    'all_tiantai_text.png')
                if(point):
                    self.F_移动到游戏区域坐标(227, 373)
                    utils.click()
                    time.sleep(1)
                    break
                else:
                    self.F_小地图寻路器([354, 247], True)
                    pyautogui.press('f9')
                    pyautogui.hotkey('alt', 'h')
                    self.F_移动到游戏区域坐标(286, 333)
                    utils.click()
                    utils.click()
                    time.sleep(1)
        else:
            self.F_使用飞行符('建邺城')
            time.sleep(1)
            self.F_小地图寻路器([58, 32], True)
            pyautogui.press('f9')
            pyautogui.hotkey('alt', 'h')
            self.F_移动到游戏区域坐标(315, 275)
            utils.click()
            utils.click()
            time.sleep(1)
            self.F_移动到游戏区域坐标(218, 370)
            utils.click()
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
            utils.rightClick()

        # self.F_选择仓库号(1)
        # time.sleep(1)
        # self.F_移动到游戏区域坐标(144, 240)
        # utils.rightClick()
        # time.sleep(1)
        # self.F_选中道具格子(1)
        # utils.rightClick()
        # time.sleep(0.5)
        # pyautogui.hotkey('alt', 'e')
        # time.sleep(0.5)
        # self.F_选中仓库道具格子(1)
        # utils.rightClick()
        time.sleep(0.5)
        self.F_移动到游戏区域坐标(689, 142)
        utils.click()

    def 切换有空仓库(self):
        while (记录值['满仓库遍历值'] <= 25):
            print(记录值['满仓库遍历值'])
            self.F_选择仓库号(记录值['满仓库遍历值'])
            time.sleep(0.2)
            if(self.findImgInWindow("all-cangku-gezi.png", 0.99, area=(323, 370, 49, 49)) == None):
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

    def 获取当前地图2(self):
        area = [self.windowArea[0] + 27, self.windowArea[1] + 23, 101, 19]
        path = self.F_窗口区域截图('temp_orc_info.png', area)
        ret = baiduApi.cnocr文字识别2(path)
        print(ret)
        if(ret != None):
            if("酒店" in ret):
                return "酒店"

    def F_获取小地图寻路坐标(self):
        ret = baiduApi.F_大漠小地图寻路坐标识别([self.windowArea[0], self.windowArea[1],
                                      self.windowArea[0] + 800,  self.windowArea[1] + 600])
        if(ret != None):
            ponit = ret.split(',')
            return ponit

    def 任务栏点击(self, x, y):
        pyautogui.hotkey('alt', 'f')
        self.F_移动到游戏区域坐标(x, y)
        pyautogui.hotkey('alt', 'f')
        time.sleep(0.5)
        utils.click()

    def F_获取任务位置和坐标(self, str):
        map = ""
        if("花果山" in str):
            map = "花果山"
        if("宝象国" in str):
            map = "宝象国"
        elif("五庄观" in str or '庄观' in str):
            map = "五庄观"
        elif("江南野外" in str or "野外" in str):
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
        elif("宝象国" in str):
            map = "宝象国"
        elif("长寿村" in str):
            map = "长寿村"
        elif("长寿郊外" in str or ("外" in str and "长寿" in str)):
            map = "长寿郊外"
        elif("女国" in str):
            map = "西梁女国"
        elif("化生寺" in str):
            map = "化生寺"
        elif("地府" in str):
            map = "地府"
        elif("地狱迷宫" in str or ("地" in str and "迷宫" in str)):
            map = "地狱迷宫"
        elif("碗子山" in str):
            map = "碗子山"
        elif("女娲" in str):
            map = "女娲神迹"
        elif("天宫" in str):
            map = "天宫"
        elif("海底迷宫" in str):
            map = "海底迷宫"
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

    def F_点击自动2(self):
        self.F_移动到游戏区域坐标(695, 385)
        # utils.click()
        pyautogui.click()
        self.F_移动到游戏区域坐标(339, 552)
        # utils.click()
        pyautogui.click()

    def F_点击自动(self):
        self.F_移动到游戏区域坐标(695, 385)
        utils.click()
        self.F_移动到游戏区域坐标(339, 552)
        utils.click()

    def F_点击小地图出入口按钮(self):
        pyautogui.press('tab')
        time.sleep(1)
        point = self.findImgInWindowReturnWindowPoint('all_font_intro.png')
        if(point):
            self.F_移动到游戏区域坐标(point[0], point[1])
            utils.click()
        pyautogui.press('tab')

    def 准备工作(self):
        pyautogui.hotkey('alt', '~')
        self.F_移动到游戏区域坐标(339, 552)
        utils.click()

    def F_查看摄妖香分钟(self):
        self.F_移动到游戏区域坐标(574, 201)
        self.F_移动到游戏区域坐标(658, 126)
        time.sleep(0.2)
        ret = baiduApi.F_大漠摄妖香分钟识别([self.windowArea[0]+543, self.windowArea[1]+100,
                                    self.windowArea[0] + 600,  self.windowArea[1] + 145])
        if(ret != None):
            print(ret)
            return ret

    def F_获取灯谜(self):
        logUtil.chLog('F_获取灯谜')
        result = pyautogui.locateOnScreen(
            self.pyImageDir + self.F_获取设备图片('all-yuanxiao-dati.png'), grayscale=True, confidence=0.75)
        if(result != None):
            print('找到')
            print(result)
            while True:
                self.F_移动到游戏区域坐标(450, 240)
                time.sleep(1)
                ret = pyautogui.locateOnScreen(
                    self.pyImageDir + self.F_获取设备图片('all-yuanxiao-dati2.png'), grayscale=True, confidence=0.9)
                if (ret != None):
                    print(result)
                if(ret != None and result != None):
                    print('?????')
                    top = ret[1] - result[1]
                    left = ret[0] - result[0]
                    print(left)
                    print(top)
                    if(top > 342):
                        print('c, d')
                    if(left < 650):
                        print('a, c')
                    if(top > 342 and left < 650):
                        self.F_移动到游戏区域坐标(379, 383)
                        # utils.click()
                    if(top > 342 and left > 650):
                        self.F_移动到游戏区域坐标(589, 383)
                        # utils.click()
                    if(top < 342 and left < 650):
                        self.F_移动到游戏区域坐标(383, 311)
                        # utils.click()
                    if(top < 342 and left > 650):
                        self.F_移动到游戏区域坐标(586, 308)
                    time.sleep(0.5)
                    utils.click()


def 挖图导航(window, map):
    if(map == '江南野外'):
        window.F_导航到江南野外()
    elif(map == '狮驼岭'):
        window.F_导航到狮驼岭()
    elif(map == '大唐国境'):
        window.F_导航到大唐国境()
    elif(map == '朱紫国'):
        window.F_导航到朱紫国()
    elif(map == '北俱芦洲'):
        window.F_导航到北俱芦洲()
    elif(map == '长寿郊外'):
        window.F_导航到长寿郊外()
    elif(map == '麒麟山'):
        window.F_导航到麒麟山()
    elif(map == '普陀山'):
        window.F_导航到普陀山()
    elif(map == '墨家村'):
        window.F_导航到墨家村()
    elif(map == '花果山'):
        window.F_导航到花果山()
    elif(map == '傲来国'):
        window.F_导航到傲来国()
    elif(map == '女儿村'):
        window.F_导航到女儿村()
    elif(map == '建邺城'):
        window.F_导航到建邺城()
    elif(map == '东海湾'):
        window.F_导航到东海湾()
    elif(map == '大唐境外'):
        window.F_导航到大唐境外()
    elif(map == '五庄观'):
        window.F_导航到五庄观()


if __name__ == '__main__':
    time.sleep(3)
    window = MHWindow(1)
    window.findMhWindow()
    # point = baiduApi.F_人物位置识别([window.windowArea[0], window.windowArea[1],
    #                            window.windowArea[0] + 800,  window.windowArea[1] + 600])
    # print(point)
    pyautogui.press('f9')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'h')
    time.sleep(0.5)
    # window.F_卖体力()
    # pyautogui.press('f9')
    # time.sleep(1)
    # window.F_移动到游戏区域坐标(324, 307)
    # utils.click()
    # time.sleep(1)
    # map = '花果山'
    # if(window.获取当前地图() != map):
    #     挖图导航(window, map)
    #     time.sleep(2)
    #     if(window.获取当前地图() != map):
    #         挖图导航(window, map)
