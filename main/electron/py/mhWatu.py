# coding=utf-8

import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
import utils
import networkApi
import mouse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def F_获取任务位置和坐标(str):
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
    elif("长寿郊外" in str or ("外" in str and "长寿" in str)):
        map = "长寿郊外"
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
        print("An exception occurred")
        return [map, [0, 0]]


def F_获取宝图信息(window=None, restart=0):
    time.sleep(2)
    if(window == None):
        MHWindow = mhWindow.MHWindow
        window = MHWindow(1)
        window.findMhWindow()
    window.focusWindow()
    if(restart != 1):
        window.医宝宝()
    time.sleep(0.5)
    utils.click()
    pyautogui.hotkey('alt', 'e')
    window.focusWindow()
    time.sleep(1)
    points = window.findImgsInWindow('daoju_baotu.png', confidence=0.75)
    res = []
    for point in points:
        mapAndpoint = 识别位置信息(window, point)
        if(mapAndpoint != None or mapAndpoint[1][0] == 0):
            mapAndpoint = 识别位置信息(window, point)
        print(mapAndpoint)
        res.append(mapAndpoint)
    networkApi.sendWatuInfoLogo(window.gameId, len(points))
    jsonArr = json.dumps(res, ensure_ascii=False)
    pyautogui.hotkey('alt', 'e')
    window.focusWindow()
    map = res[0][0]
    print(map)
    time.sleep(1)
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
    time.sleep(1)
    window.F_点击小地图出入口按钮()
    logUtil.chLog('mhWatu result:start' + jsonArr + 'end')


def 识别位置信息(window, point):
    window.pointMove(point[0], point[1])
    time.sleep(0.2)
    宝图位置信息 = [window.windowArea[0], window.windowArea[1],
              window.windowArea[0] + 600, window.windowArea[1] + 600]
    ret = window.F_宝图文字识别(宝图位置信息)
    logUtil.chLog(ret)
    mapAndpoint = F_获取任务位置和坐标(ret)
    return mapAndpoint


mapDict = {
    '狮驼岭': "map_top_shituo.png",
    '建邺城': "map_top_jianye.png",
    '北俱芦洲': "map_top_beiju.png",
    '大唐境外': "map_top_jingwai.png",
    '大唐国境': "map_top_guojing.png",
    '朱紫国': "map_top_zhuziguo.png",
    '五庄观': "map_top_wuzhuangguan.png",
    '花果山': "map_top_huoguoshan.png",
    '傲来国': "map_top_aolaiguo.png",
    '麒麟山': "map_top_qilingshan.png",
    '普陀山': "map_top_putuo.png",
    '墨家村': "map_top_mojiacun.png",
    '长寿郊外': "map_top_jiaowai.png",
    '江南野外': "map_top_jiangnanyewai.png",
    '江南野外': "map_top_jiangnanyewai.png",
    '女儿村': "map_top_nvercun.png",
    '东海湾': "map_top_donghaiwan.png",
}

mapDictEntrance = {
    '五庄观': [26, 73],
    '江南野外': [26, 108],
    '普陀山': [87, 4],
    '北俱芦洲': [306, 263],
    '东海湾': [222, 263],
    '大唐境外': [14, 53],
    '建邺城': [31, 267],
    '长寿郊外': [272, 32],
    '女儿村': [292, 322],
    '大唐国境': [361, 199],
    '麒麟山': [347, 266],
    '狮驼岭': [347, 19],
    '东海湾': [186, 235],
    '大唐境外': [0, 0],
    '朱紫国': [314, 56],
    '花果山': [0, 200],
    '墨家村': [167, 324],
    '傲来国': [0, 0],
    '长寿村': [0, 0],
}


def F_点击宝图(window, userId, map, x, y, ox, oy, num):
    userId = str(userId)
    print('点击小地图', userId, x, y)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, userId)
    window.findMhWindow()
    window.focusWindow()
    # window.ClickInWindow(mapTopLeft[0], mapTopLeft[1])
    # window.F_打开地图()
    time.sleep(0.3)
    pyautogui.press('tab')
    time.sleep(1)
    point = window.findImgInWindow(mapDict.get(map))
    window.pointMove(point[0] + x, point[1] + y, 移动到输入框=True)
    utils.click()
    window.F_小地图寻路器([ox, oy], openTab=True, 是否模糊查询=True)
    window.F_选中道具格子(int(num))
    utils.rightClick()
    # utils.rightClick()
    window.F_自动战斗()
    # window.F_吃药()
    pyautogui.hotkey('alt', 'e')


def F_获取最近的坐标点(x, y, other):
    for item in other:
        distance = (item.get('realX') - x) * (item.get('realX') -
                                              x) + (item.get('realY') - y)*(item.get('realY') - y)
        item['distance'] = distance
    sortother = sorted(other, key=lambda item: item['distance'])
    logUtil.chLog(sortother)
    newOther = sortother[1:]
    # todo
    point = sortother[0]
    return point, newOther


def F_点击宝图并寻路(window, map, x, y, ox, oy, num, other):
    if(x == 0 or y == 0):
        point, newOther = F_获取最近的坐标点(x, y, other)
        F_点击宝图并寻路(window, map, point['realX'],
                  point['realY'], point['orgPointX'], point['orgPointY'], point['index'], newOther)
    else:
        logUtil.chLog('F_点击宝图并寻路:' + str(num))
        pyautogui.moveTo(
            window.windowArea[0] + 400, window.windowArea[1] + 300)
        pyautogui.press('tab')
        time.sleep(1)
        point = window.findImgInWindow(mapDict.get(map))
        if(point == None):
            point = window.findImgInWindow(mapDict.get(map))
        if(point == None):
            pyautogui.press('tab')
            time.sleep(1)
            point = window.findImgInWindow(mapDict.get(map))
        mouse.move(point[0] + x, point[1] + y)
        time.sleep(0.5)
        utils.click()
        window.F_小地图寻路器([ox, oy], openTab=True, 是否模糊查询=True)
        pyautogui.moveTo(
            window.windowArea[0] + 400, window.windowArea[1] + 300)
        window.F_选中道具格子(int(num))
        utils.rightClick()
        # utils.rightClick()
        window.F_自动战斗()
        # window.F_吃药()
        pyautogui.hotkey('alt', 'e')
        if(len(other) > 0):
            point, newOther = F_获取最近的坐标点(x, y, other)
            F_点击宝图并寻路(window, map, point['realX'],
                      point['realY'], point['orgPointX'], point['orgPointY'], point['index'], newOther)


loop = 1


def F_点击小地图(map, x, y, ox, oy, num, other, isBeen, 仓库位置='长安城'):
    print('点击小地图', x, y)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    window.focusWindow()
    if(other == None):
        F_点击宝图(window, map, x, y, ox, oy, num)
    else:
        if num == 1:
            firstPoint = {"realX": x, "realY": y,
                          "orgPointX": ox, "orgPointY": oy, "index": num}
            if other != None:
                other.append(firstPoint)
                entrancePoint = mapDictEntrance.get(map)
                point, newOther = F_获取最近的坐标点(
                    entrancePoint[0], entrancePoint[1], other)
                F_点击宝图并寻路(window, map,
                          point['realX'], point['realY'], point['orgPointX'], point['orgPointY'], point['index'], newOther)
        else:
            F_点击宝图并寻路(window, map,
                      x, y, ox, oy, num, other)
    window.F_点击小地图出入口按钮()
    接货id = networkApi.获取空闲接货人ID(window.gameId, '接货')
    if(接货id != None):
        window.F_回仓库丢小号(接货id, 仓库位置)
    else:
        window.F_回仓库放东西(map, 仓库位置)
    if(isBeen):
        F_小蜜蜂模式(仓库位置, 0, window)


def F_邀请发图(window):
    pyautogui.hotkey('alt', 'f')
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(694, 384)
    utils.rightClick()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(355, 440)
    utils.click()
    window.F_移动到游戏区域坐标(403, 250)
    utils.rightClick()
    window.F_移动到游戏区域坐标(694, 384)
    utils.click()
    pyautogui.press('1')
    pyautogui.press('enter')
    pyautogui.hotkey('alt', 'f')


def F_小蜜蜂模式(仓库位置, restart=0, window=None):
    time.sleep(3)
    if(window == None):
        logUtil.chLog('开始发车')
        MHWindow = mhWindow.MHWindow
        window = MHWindow(1)
        window.findMhWindow()
    else:
        logUtil.chLog('继续发车')
    if(restart != 1):
        if(window.gameId != ''):
            networkApi.doUpdateRoleStatus(window.gameId, '空闲')
    window.focusWindow()
    time.sleep(0.5)
    window.F_使用酒肆和打坐()
    time.sleep(0.5)
    while(True):
        window.F_打开道具()
        time.sleep(1)
        point = window.findImgInWindow('daoju_baotu.png')
        if(point != None and point[0] > 0):
            if(restart != 1):
                time.sleep(10)
            window.F_吃香()
            pyautogui.hotkey('alt', 'e')
            window.F_点击自动()
            F_获取宝图信息(window, restart=restart)
            break
        else:
            window.findMhWindow()
            time.sleep(10)


if __name__ == '__main__':

    fire.Fire({
        'info': F_获取宝图信息,
        'clickMap': F_点击小地图,
        'bee': F_小蜜蜂模式
    })
