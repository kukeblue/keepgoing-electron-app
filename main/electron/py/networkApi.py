# coding=utf-8

import json
import requests
host = 'http://192.168.0.13:3000/api/client/'


def sendWatuLog(taskNo, deviceId, note):
    url = host + "add_task_log"
    payload = "{\"imei\": \"0\",\"nickName\": \"" + nickName + "\",  \"taskNo\": \"" + taskNo + "\",  \"deviceId\": 1,  \"accountId\": " + \
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


def getDeviceOneWatuTask(deviceId):
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
        print(res.get('data').get("taskName"))
        global nickName
        nickName = res.get('data').get("accountNickName")
        sendWatuLog(res.get('data').get("taskNo"), deviceId, "准备完毕")


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
        print(res.get('data').get("taskName"))
        global nickName
        nickName = res.get('data').get("accountNickName")
        sendWatuLog(res.get('data').get("taskNo"), deviceId, "准备完毕")


def doStartWatuTask(deviceId):
    url = host + "get_one_task"
    payload = "{\"deviceId\":" + deviceId + ",\"name\": \"主线挖图\"}"
    headers = {
        'content-type': "application/json",
    }
    response = requests.request(
        "POST", url, data=payload.encode(), headers=headers)
    res = json.loads(response.text)
    if(res.get('status') == 0):
        print(res.get('data').get("taskName"))
        global nickName
        nickName = res.get('data').get("accountNickName")
        sendWatuLog(res.get('data').get("taskNo"), deviceId, "开始挖图")


doStartWatuTask('9')
