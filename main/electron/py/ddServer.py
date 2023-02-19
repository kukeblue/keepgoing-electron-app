# 导入socket模块
import socket
from ctypes import *
import time
import os
import json
import fire

print("Load DD!")
pyHome = __file__.strip('ddServer.pyc')

def killport(port):
    command = "kill -9 $(netstat -nlp | grep :"+str(port) + \
        " | awk '{print $7}' | awk -F'/' '{{ print $1 }}')"
    os.system(command)

def start(userid, maxBaotu = 0):
    if(os.path.exists(r"C:\config.txt")):
        fp = open(r"C:\config.txt", 'a+')
        fp.seek(0, 0)
        config = json.loads(fp.read())
        if(config['userId'] != userid):
            config['userId'] = userid
        print(maxBaotu)
        print(config['maxBaotu'])
        if(config['maxBaotu'] != maxBaotu):
            config['maxBaotu'] = maxBaotu
        configNew = json.dumps(config, ensure_ascii=False)
        fp.truncate(0)
        fp.write(configNew)
    else:
        print('生成配置文件')
        fp = open(r"C:\config.txt", "w+")
        config = {
            "userId": userid,
            "maxBaotu": maxBaotu,
        }
        configStr = json.dumps(config, ensure_ascii=False)
        fp.write(configStr)
        fp.close()
    
    with os.popen('netstat -aon|findstr "61234"') as res:
        res = res.read().split('\n')
        result = []
        for line in res:
            temp = [i for i in line.split(' ') if i != '']
            if len(temp) > 4:
                result.append(temp[4])
    
    if(len(result) > 0):
        return
    else:
        dd_dll = windll.LoadLibrary(pyHome + '\config\DD94687.64.dll')
        time.sleep(2)

        st = dd_dll.DD_btn(0)  # DD Initialize
        if st == 1:
            print("OK")
        else:
            print("Error")
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 61234))
            s.listen(128) 
            s1, addr = s.accept() 
            print(addr)
            while True:
                data = s1.recv(1024)
                recv_content = data.decode(encoding="utf-8")
                if(recv_content == 'click'):
                    dd_dll.DD_btn(1)
                    dd_dll.DD_btn(2)
                    time.sleep(0.2)
                elif(recv_content == 'rightClick'):
                    dd_dll.DD_btn(4)
                    dd_dll.DD_btn(8)
                    time.sleep(0.2)
                elif(recv_content == 'doubleClick'):
                    dd_dll.DD_btn(1)
                    dd_dll.DD_btn(2)
                    dd_dll.DD_btn(1)
                    dd_dll.DD_btn(2)
                    time.sleep(0.2)
                send_data = "好的，消息已收到".encode(encoding="utf-8")
                s1.send(send_data)
        except:
            print('error')

if __name__ == '__main__':
    fire.Fire({
        'start': start,
    })
    