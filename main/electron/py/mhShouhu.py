from ast import While
from ctypes import util
import wmi
import os
import time
import logUtil
import mhWindow


def printCmd(process):
    print(process)
    print(f'{process.Handle} | {process.Caption} | {process.CommandLine}')


def monirtor(prop1, par=None):
    tmpmon = []
    c = wmi.WMI()
    for process in c.Win32_Process(name=prop1):
        if par is None:
            # printCmd(process)
            tmpmon.append(process)
            # print(f'{process.Handle} | {process.Caption} | {process.CommandLine}')
        else:
            if str(process.CommandLine).find(par) >= 0:
                # print(
                #     f'{process.Handle} | {process.Caption} | {process.CommandLine}')
                # printCmd(process)
                tmpmon.append(process)
    return tmpmon


def killtask(pid):
    os.system(f"taskkill /F /pid {pid} -t")


def show(par):
    pid = os.getpid()
    print(pid)
    tmp2 = monirtor('python.exe', par)
    for v in tmp2:
        if(str(v.Handle) != str(pid) and ('mhShouhu' in v.CommandLine)):
            return
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow(1)
    window.findMhWindow()
    time.sleep(5)
    坐标 = ""
    重启计数器 = 40
    检查次数 = 0
    是否设置上次命令 = False
    process = None
    logUtil.chLog('开启守护进程')
    while True:
        # print(f"pid | exe | cmd")
        tmp2 = monirtor('python.exe', par)
        mhWatuStarting = False
        for v in tmp2:
            # printCmd(v)
            if('mhWatu' in v.CommandLine):
                process2 = v
                mhWatuStarting = True
                if(是否设置上次命令 == False):
                    是否设置上次命令 = True
                    if('bee' in process2.CommandLine):
                        with open(window.pyImageDir + '/temp/912.txt', "w", encoding='utf-8') as f:
                            f.write(process2.CommandLine)
                            f.close()
                if(process == None or process2.Handle != process.Handle):
                    process = process2
                break
        if(mhWatuStarting):
            point = window.获取当前坐标()
            当前坐标 = str(point)
            if(当前坐标 == 坐标):
                print('重启计数器' + str(重启计数器))
                重启计数器 = 重启计数器 - 1
            else:
                坐标 = 当前坐标
                重启计数器 = 40
            if(重启计数器 == 30 and 当前坐标 != 6530):
                重启计数器 = 40
                # print(f'{process.Handle} | {v.Caption} | {process.CommandLine}')
                killtask(process.Handle)
                time.sleep(3)
                # print('执行：' + process.CommandLine + ' ' +
                #       str(window.handle) + ' ' + window.gameId)
                # with open(window.pyImageDir + '/temp/912.txt', "r", encoding='utf-8') as f:
                #     window.focusWindow2()
                #     pyautogui.click()
                #     utils.click()
                #     os.popen(f.read())
            elif(重启计数器 == 0):
                重启计数器 = 40
                # print(f'{process.Handle} | {v.Caption} | {process.CommandLine}')
                killtask(process.Handle)
                time.sleep(3)
                # print('执行：' + process.CommandLine + ' ' +
                #       str(window.handle) + ' ' + window.gameId)
                # with open(window.pyImageDir + '/temp/912.txt', "r", encoding='utf-8') as f:
                #     window.focusWindow2()
                #     pyautogui.click()
                #     utils.click()
                #     os.popen(f.read())
        else:
            if(process == None):
                break
            检查次数 = 检查次数 + 1
            if(检查次数 == 2):
                检查次数 = 0
                with open(window.pyImageDir + '/temp/912.txt', "r", encoding='utf-8') as f:
                    # window.focusWindow2()
                    # util.click()
                    # pyautogui.click()
                    os.popen(f.read())
        time.sleep(60)


def help():
    print('qpy query python bakserver')
    print('\t-l par query par')
    print('\t-a show all')
    print('\t-lk par 终止查询到的程序')


if __name__ == "__main__":
    show('mh')
