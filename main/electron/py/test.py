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
    print(f"pid | exe | cmd")

    tmp1 = monirtor('pythonw.exe',par)
    tmp2 = monirtor('python.exe',par)
    for v in tmp1:
        printCmd(v)
    for v in tmp2:
        printCmd(v)

    istr = input("请输入(y/n)，终止查询到的程序：")
    if istr == 'y':
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
    alen = len(sys.argv)
    if alen > 1:
        if sys.argv[1] == '-l':
            if alen <= 2:
                print('-l par is none','demo: qpy -l index')
                exit()
            else:
                show(sys.argv[2])
        elif sys.argv[1] == '-a':
            show(None)
        elif sys.argv[1] == '-k':
            if alen <= 2:
                print('-k pid is none','demo: qpy -k 121212')
                exit()
            killtask(sys.argv[2])
        elif sys.argv[1] == '-lk':
            if alen <= 2:
                print('-lk par is none','demo: qpy -lk index')
                exit()
            else:
                findKill(sys.argv[2])

        else:
            print('CommandLine no fount')
            help()
    else:
        help()
