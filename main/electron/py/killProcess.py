#! /usr/bin/python
#　-*- coding: utf-8 -*-

import os
import sys
import signal


def kill(pid):
    os.kill(int(pid), signal.SIGINT)

if __name__ == '__main__':
    args = sys.argv[1:]
    print(args[0])
    kill(args[0])

