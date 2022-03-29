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
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def F_获取任务位置和坐标(str):
    map = ""
    if("花果山" in str):
        map = "花果山"
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
    deviceId = str(deviceId)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1, deviceId)
    window.findMhWindow()
    window.focusWindow()
    point = window.checkpoint()
    print(point)
    points = window.findImgsInWindow('daoju_baotu.png')
    print(len(points))
    res = []
    for point in points:
        print(point)
        window.pointMove(point[0], point[1])
        point = window.findImgInWindow('daoju_baotu_large.png')
        print('放大宝图位置', point)
        if(point != None):
            宝图位置信息 = [point[0], point[1], 255, 50]
            # 截图 + ocr识别
            path = window.F_窗口区域截图('temp_baotu_info.png', 宝图位置信息)
            time.sleep(0.2)
            print('放大宝图位置', path)
            ret = window.F_截图文字识别(path)
            if(ret != ''):
                logUtil.chLog(ret)
                mapAndpoint = F_获取任务位置和坐标(ret)
                print(mapAndpoint)
                res.append(mapAndpoint)
    jsonArr = json.dumps(res, ensure_ascii=False)
    logUtil.chLog('mhWatu result:start' + jsonArr + 'end')


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


def F_点击宝图(deviceId, map, x, y, num):
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


def 排序(x, y):
    return -1


def F_获取最近的坐标点(x, y, other):
    for item in other:
        distance = (item.get('realX') - x) * (item.get('realX') -
                                              x) + (item.get('realY') - y)*(item.get('realY') - y)
        item['distance'] = distance
    sortother = sorted(other, key=lambda item: item['distance'])
    logUtil.chLog(sortother)
    newOther = sortother[1:]
    point = sortother[0]
    return point, newOther


def F_点击宝图并寻路(deviceId, map, x, y, num, other):
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
    window.F_是否结束寻路()
    pyautogui.press('tab')
    pyautogui.hotkey('alt', 'e')
    time.sleep(0.2)
    window.F_选中道具格子(num)
    pyautogui.rightClick()
    pyautogui.rightClick()
    window.F_自动战斗()
    pyautogui.hotkey('alt', 'e')
    if(len(other) > 0):
        point, newOther = F_获取最近的坐标点(x, y, other)
        F_点击宝图并寻路(deviceId, map, point['realX'],
                  point['realY'], point['index'], newOther)


def F_点击小地图(deviceId, map, x, y, num, other):
    if(other == None):
        F_点击宝图(deviceId, map, x, y, num)
    else:
        F_点击宝图并寻路(deviceId, map, x, y, num, other)


if __name__ == '__main__':
    # deviceId = str(11)
    # MHWindow = mhWindow.MHWindow
    # window = MHWindow(1, deviceId)
    # window.findMhWindow()
    # window.focusWindow()
    fire.Fire({
        'info': F_获取宝图信息,
        'clickMap': F_点击小地图,
    })
