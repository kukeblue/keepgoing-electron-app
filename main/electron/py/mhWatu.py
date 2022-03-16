import mhWindow
import re

def F_获取宝图位置和坐标(str):
    return re.findall("(\d+)", str)


if __name__ == '__main__':
    MHWindow = mhWindow.MHWindow
    window = MHWindow(2)
    window.findMhWindow()
    window.focusWindow()
    point = window.checkpoint()
    print(point)
    point = window.findImgInWindow('/daoju_baotu.png')
    if(point != None): 
        print(point)
        window.pointMove(point[0], point[1])
        point = window.findImgInWindow('/daoju_baotu_large.png')
        print('放大宝图位置', point)
        if(point != None):
            宝图位置信息 = [point[0], point[1], 255, 50]
            # 截图 + ocr识别
            path = window.F_窗口区域截图('temp_baotu_info.png', 宝图位置信息)
            ret = window.F_截图文字识别(path)
            print(ret)