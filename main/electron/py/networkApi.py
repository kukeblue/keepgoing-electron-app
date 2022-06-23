# coding=utf-8

from PIL import Image
import base64
import io
import random
import re
import json
from time import sleep
import requests
host = 'http://103.100.210.203:3000/api/client/'

suanHost = ''


def sendWatuLog(taskNo, deviceId, note):
    url = host + "add_task_log"
    payload = "{\"imei\": \"0\",\"nickName\": \"" + nickName + "\",  \"taskNo\": \"" + taskNo + "\",  \"deviceId\": " + deviceId + ",  \"accountId\": " + \
        deviceId + ",  \"taskName\": \"主线挖图\",  \"note\":  \"" + \
        note + "\",  \"type\": \"info\",  \"time\": 1655084688}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fe1447a3-8cbe-5a50-744d-7b016e4cd990"
    }
    response = requests.request(
        "POST", url, data=payload.encode(), headers=headers)
    print(response.text)


def doReadyWatuTask(deviceId):
    url = host + "get_one_task"
    payload = "{\"deviceId\":" + deviceId + \
        ",\"name\": \"主线挖图\",\"status\": \"进行中\"}"
    headers = {
        'content-type': "application/json",
    }
    response = requests.request(
        "POST", url, data=payload.encode(), headers=headers)
    res = json.loads(response.text)
    if(res.get('status') == 0):
        print(res.get('data').get("accountNickName"))
        global nickName
        nickName = res.get('data').get("accountNickName")
        sendWatuLog(res.get('data').get("taskNo"), deviceId, "准备完毕")


def suanGetHost():
    url = "http://3.haoi23.net/svlist.html"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "92aa8718-e119-fd3d-213e-60b20ddd59b0"
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    global suanHost
    hosts = response.text.replace("===", '').replace("+++", '')
    hosts = hosts.split('--')
    suanHost = "http://" + hosts[0]
    print(suanHost)


def getPicPoint(image_path):
    imgBase64 = encode_base64(image_path)
    ret = '失败'
    global suanHost
    url = suanHost + "/UploadBase64.aspx"
    num = str(random.randint(1, 10000))
    payload = ("userstr=18370893382%7C7WMLR2BYIKMVBRTX&gameid=6001&timeout=60&daiLi=haoi&ver=web2&key=" +
               num+"&Img=" + imgBase64).encode()
    # print(payload)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    if(response.text and '6001_' in response.text):
        tid = response.text
        for x in range(60):
            sleep(1)
            num = str(random.randint(1, 10000))
            url = suanHost + "/GetAnswer.aspx"
            payload = "id=" + tid + "&r=" + num
            print(payload)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
            }
            response = requests.request(
                "POST", url, data=payload.encode(), headers=headers)
            ret = response.text
            print(response.text)
            if(response.text != ''):
                break
    print('成功！', ret)
    return ret


def encode_base64(file):
    with open(file, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        # print(base64_data)
        # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
        base64_str = base64_data.encode('utf-8')
        return base64_str


suanGetHost()
