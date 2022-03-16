import logUtil
import mhWindow
import re
import json

def F_获取任务位置和坐标(str):
    map=""
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
    elif("东海" in str):
        map = "东海湾"
    elif("建" in str):
        map = "建邺城"
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



    

def F_获取宝图信息():
    MHWindow = mhWindow.MHWindow
    window = MHWindow(2)
    window.findMhWindow()
    window.focusWindow()
    point = window.checkpoint()
    print(point)
    points = window.findImgsInWindow('/daoju_baotu.png')
    print(len(points))
    res = []
    for point in points:
        print(point)
        window.pointMove(point[0], point[1])
        point = window.findImgInWindow('/daoju_baotu_large.png')
        print('放大宝图位置', point)
        if(point != None):
            宝图位置信息 = [point[0], point[1], 255, 50]
            # 截图 + ocr识别
            path = window.F_窗口区域截图('temp_baotu_info.png', 宝图位置信息)
            ret = window.F_截图文字识别(path)
            if(ret != ''):
                logUtil.chLog('mhWatu:' + ret) 
                mapAndpoint = F_获取任务位置和坐标(ret)
                print(mapAndpoint)
                res.append(mapAndpoint)
    jsonArr = json.dumps(res,ensure_ascii=False)  
    logUtil.chLog('mhWatu result:start' + jsonArr + 'end') 


if __name__ == '__main__':
    F_获取宝图信息()
