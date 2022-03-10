import time
import logUtil
import os
import logUtil

pid = os.getpid()
logUtil.chLog('pythonPid|asyncTest|' + str(pid))
while True:
    logUtil.chLog('test2')
    time.sleep(1)
