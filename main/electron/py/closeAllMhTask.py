import wmi
import os
import time
import sys

def printCmd(process):
    print(process)
    print(f'{process.Handle} | {process.Caption} | {process.CommandLine}')

def monirtor(prop1,par=None):
    tmpmon = []
    c = wmi.WMI()
    for process in c.Win32_Process(name=prop1):
        if par is None:
            # printCmd(process)
            tmpmon.append(process)
            # print(f'{process.Handle} | {process.Caption} | {process.CommandLine}')
        else:
            if str(process.CommandLine).find(par) >= 0:
                # print(f'{process.Handle} | {process.Caption} | {process.CommandLine}')
                # printCmd(process)
                tmpmon.append(process)
    return tmpmon

def killtask(pid):
    os.system(f"taskkill /F /pid {pid} -t")

def show(par):
    print(f"pid | exe | cmd")

    tmp1 = monirtor('pythonw.exe',par)
    tmp2 = monirtor('python.exe',par)
    for v in tmp1:
        printCmd(v)
    for v in tmp2:
        printCmd(v)



def findKill(par):
    tmp1 = monirtor('pythonw.exe',par)
    tmp2 = monirtor('python.exe',par)
    for v in tmp1:
        printCmd(v)
    for v in tmp2:
        printCmd(v)
    for v in tmp1:
        killtask(v.Handle)
    for v in tmp2:
        killtask(v.Handle)


def help():
    print('qpy query python bakserver')
    print('\t-l par query par')
    print('\t-a show all')
    print('\t-lk par 终止查询到的程序')

if __name__ == "__main__":
   findKill('mh')
