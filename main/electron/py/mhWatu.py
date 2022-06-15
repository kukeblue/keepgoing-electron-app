# coding=utf-8
from cv2 import log
import logUtil
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
import networkApi
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
        return [map, [0, 0]]
        print("An exception occurred")


def F_获取宝图信息(deviceId):
    time.sleep(3)
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    window.F_使用长安城飞行棋('化生寺出口')
    pyautogui.hotkey('alt', 'e')
    time.sleep(1)
    point = window.checkpoint()
    points = window.findImgsInWindow('daoju_baotu.png')
    res = []
    for point in points:
        mapAndpoint = 识别位置信息(window, point)
        if(mapAndpoint != None or mapAndpoint[1][0] == 0):
            mapAndpoint = 识别位置信息(window, point)
        print(mapAndpoint)
        res.append(mapAndpoint)
    jsonArr = json.dumps(res, ensure_ascii=False)
    pyautogui.hotkey('alt', 'e')
    map = res[0][0]
    print(map)
    time.sleep(3)
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

    logUtil.chLog('mhWatu result:start' + jsonArr + 'end')


def 识别位置信息(window, point):
    print(point)
    window.pointMove(point[0], point[1])
    time.sleep(0.2)
    if(point != None):
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
    '朱紫国': [200, 200],
    '花果山': [0, 200],
    '墨家村': [50, 200],
    '傲来国': [0, 0],
    '长寿村': [0, 0],
}


def F_点击宝图(window, deviceId, map, x, y, num):
    deviceId = str(deviceId)
    print('点击小地图', deviceId, x, y)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    # window.ClickInWindow(mapTopLeft[0], mapTopLeft[1])
    pyautogui.press('tab')
    time.sleep(1)
    point = window.findImgInWindow(mapDict.get(map))
    window.pointMove(point[0] + x, point[1] + y)
    pyautogui.click()
    pyautogui.click()
    pyautogui.press('tab')


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


def F_点击宝图并寻路(window, deviceId, map, x, y, num, other):
    if(x == 0 or y == 0):
        point, newOther = F_获取最近的坐标点(x, y, other)
        F_点击宝图并寻路(window, deviceId, map, point['realX'],
                  point['realY'], point['index'], newOther)
    else:
        logUtil.chLog('F_点击宝图并寻路:' + str(num))
        # window.ClickInWindow(mapTopLeft[0], mapTopLeft[1])
        pyautogui.moveTo(
            window.windowArea[0] + 400, window.windowArea[1] + 300)
        pyautogui.press('tab')
        time.sleep(1)
        point = window.findImgInWindow(mapDict.get(map))
        if(point == None):
            point = window.findImgInWindow(mapDict.get(map))
        window.pointMove(point[0] + x, point[1] + y)
        pyautogui.click()
        pyautogui.click()
        pyautogui.moveTo(
            window.windowArea[0] + 400, window.windowArea[1] + 300)
        window.F_是否结束寻路()
        pyautogui.press('tab')
        window.F_选中道具格子(int(num))
        pyautogui.rightClick()
        # pyautogui.rightClick()
        window.F_自动战斗()
        pyautogui.hotkey('alt', 'e')
        if(len(other) > 0):
            point, newOther = F_获取最近的坐标点(x, y, other)
            F_点击宝图并寻路(window, deviceId, map, point['realX'],
                      point['realY'], point['index'], newOther)


num = 1


def F_点击小地图(deviceId, map, x, y, num, other, isBeen):
    deviceId = str(deviceId)
    print('点击小地图', deviceId, x, y)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    if(other == None):
        F_点击宝图(window, deviceId, map, x, y, num)
    else:
        if num == 1:
            firstPoint = {"realX": x, "realY": y, "index": num}
            if other != None:
                other.append(firstPoint)
                entrancePoint = mapDictEntrance.get(map)
                point, newOther = F_获取最近的坐标点(
                    entrancePoint[0], entrancePoint[1], other)
                F_点击宝图并寻路(window, deviceId, map,
                          point['realX'], point['realY'], point['index'], newOther)
    window.F_回天台放东西(map)
    window.F_选中道具格子(15)
    if(isBeen):
        # 小蜜蜂模式必须图满了才能发车
        networkApi.doReadyWatuTask(deviceId)
        while(True):
            time.sleep(20)
            if(num > 30):
                break
            num = num + 1
            # 关闭打开
            pyautogui.hotkey('alt', 'e')
            time.sleep(0.1)
            pyautogui.hotkey('alt', 'e')
            point = window.findImgInWindow('daoju_baotu_large.png')
            if(point != None and point[0] > 0):
                pyautogui.hotkey('alt', 'e')
                window.F_移动到游戏区域坐标(376, 344)
                pyautogui.click()
                F_小蜜蜂模式(deviceId)
                break
            print('等待宝图')


def F_邀请发图(window):
    pyautogui.hotkey('alt', 'f')
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(694, 384)
    pyautogui.rightClick()
    time.sleep(0.5)
    window.F_移动到游戏区域坐标(355, 440)
    pyautogui.click()
    window.F_移动到游戏区域坐标(403, 250)
    pyautogui.rightClick()
    window.F_移动到游戏区域坐标(694, 384)
    pyautogui.click()
    pyautogui.press('1')
    pyautogui.press('enter')
    pyautogui.hotkey('alt', 'f')


def F_小蜜蜂模式(deviceId):
    F_获取宝图信息(deviceId)


if __name__ == '__main__':
    fire.Fire({
        'info': F_获取宝图信息,
        'clickMap': F_点击小地图,
        'bee': F_小蜜蜂模式
    })
