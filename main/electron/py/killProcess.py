#! /usr/bin/python
#　-*- coding: utf-8 -*-

import os
import sys
import signal


def kill(pid):

    try:
        a = os.kill(int(pid), signal.SIGKILL)
        # a = os.kill(pid, signal.9) #　与上等效
        print("1")
    except:
        print("0")

if __name__ == '__main__':
    args = sys.argv[1:]
    print(args[0])
    kill(args[0])

