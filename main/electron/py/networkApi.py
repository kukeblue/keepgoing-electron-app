# coding=utf-8

import sys
import base64
import random
import json
import time
import requests
import logUtil
from urllib import parse

host = 'http://192.168.22.101:3000/api/client/'
suanHost = ''


pyHome = __file__.strip('networkApi.pyc')

pyZhikuDir2 = pyHome + 'config\images'
if(pyZhikuDir2[0] == ":"):
    pyZhikuDir2 = "C" + pyZhikuDir2



def chRequest(method, url, data, headers):
    while True:  # 一直循环，知道访问站点成功
        try:
            res = requests.request(
                method, url, data=data, headers=headers, timeout=20)
            return res
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except:
            print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(3)


def sendWatuInfoLogo(nickName, taskCount):
    taskCount = str(taskCount)
    note = ''
    print(nickName)
    url = host + "add_task_log"
    taskNo = '0'
    deviceId = '0'
    payload = "{\"imei\": \"0\",\"nickName\": \"" + nickName + "\",  \"taskCount\": \"" + taskCount + "\", \"taskNo\": \"" + taskNo + "\",  \"deviceId\": " + deviceId + ",  \"accountId\": " + \
        deviceId + ",  \"taskName\": \"挖图扫描\",  \"note\":  \"" + \
        note + "\",  \"type\": \"watuScan\",  \"time\": 1655084688}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fe1447a3-8cbe-5a50-744d-7b016e4cd990"
    }
    response = chRequest(
        "POST", url, payload.encode(), headers)
    print(response.text)
    res = json.loads(response.text)
    if(res.get('status') != 0):
        sys.exit(0)

def checkGameId(gameId, level, gameServer, name):
    fp = open(r"C:\config.txt", 'a+')
    fp.seek(0, 0)
    config = json.loads(fp.read())
    fp.close()
    userId = str(config["userId"])
    url = host + "check_account_and_role2"
    payload = "{\"userId\": \"" + userId + "\", \"name\": \"" + name + "\", \"gameId\": \"" + gameId + "\", \"level\": \"" + level + "\", \n\t\"gameServer\": \""+gameServer+"\"\n}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fe1447a3-8cbe-5a50-744d-7b016e4cd990"
    }
    response = chRequest(
        "POST", url, payload.encode(), headers)
    print(response.text)
    res = json.loads(response.text)
    if(res.get('status') != 0):
        sys.exit(0)
   
 
    


def sendWatuProfit(nickName, note):
    print(nickName, note)
    url = host + "add_task_log"
    taskNo = '0'
    deviceId = '0'
    payload = "{\"imei\": \"0\",\"nickName\": \"" + nickName + "\",  \"taskNo\": \"" + taskNo + "\",  \"deviceId\": " + deviceId + ",  \"accountId\": " + \
        deviceId + ",  \"taskName\": \"挖图收益\",  \"note\":  \"" + \
        note + "\",  \"type\": \"profit\",  \"time\": 1655084688}"
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "fe1447a3-8cbe-5a50-744d-7b016e4cd990"
    }
    response = chRequest(
        "POST", url, payload.encode(), headers)
    print(response.text)
    res = json.loads(response.text)
    if(res.get('status') == 0):
        print('success')
        print(res.get('data').get('monitor').get('baotuCount'))
        fp = open(r"C:\config.txt", 'a+')
        fp.seek(0, 0)
        config = json.loads(fp.read())
        maxBaotu = str(config["maxBaotu"])
        baotuCount = res.get('data').get('monitor').get('baotuCount')
        fp.close()
        if(int(baotuCount) > int(maxBaotu)):
           
            return True
    time.sleep(3)   

def 获取空闲接货人ID(gameId, work):
    while True:
        print('获取空闲接货人')
        print(gameId)
        print(work)
        url = host + "get_one_free_game_role"
        payload = "{\n\t\"gameId\": \""+gameId + \
            "\",\n\t\"work\": \""+work+"\"\n}"
        headers = {
            'content-type': "application/json",
        }
        response = chRequest(
            "POST", url, payload.encode(), headers)
        print(response.text)
        res = json.loads(response.text)
        if(res.get('status') == 0):
            print('success')
            return res.get('gameId')
        time.sleep(3)


def doUpdateRoleStatus(gameId, status):
    logUtil.chLog('修改角色状态')
    logUtil.chLog(gameId)
    logUtil.chLog(status)
    url = host + "update_game_role_status"
    payload = "{\n\t\"gameId\": \""+gameId + \
        "\",\n\t\"status\": \""+status+"\"\n}"
    headers = {
        'content-type': "application/json",
    }
    response = chRequest(
        "POST", url, payload.encode(), headers)
    print(response.text)
    res = json.loads(response.text)
    if(res.get('status') == 0):
        print('success')
        return True


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
    payload = "userstr=18370893382%7C7WMLR2BYIKMVBRTX&gameid=6001&timeout=60&daiLi=haoi&ver=web2&key=" + \
        num+"&Img=" + imgBase64
    # print(payload)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    response = chRequest("POST", url, data=payload, headers=headers)
    print(response.text)

    if(response.text and '6001_' in response.text):
        tid = response.text
        for x in range(60):
            time.sleep(1)
            num = str(random.randint(1, 10000))
            url = suanHost + "/GetAnswer.aspx"
            payload = "id=" + tid + "&r=" + num
            print(payload)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
            }
            response = chRequest(
                "POST", url, data=payload.encode(), headers=headers)
            ret = response.text
            print(response.text)
            if(response.text != ''):
                break
    print('成功！', ret)
    return ret


def encode_base64(file):
    with open(file, 'rb') as fin:  # 第一个参数为图片全路径或相对路径
        image_data = fin.read()
        base64_data_bytes = base64.b64encode(image_data)
        base64_data_str = base64_data_bytes.decode()
        return parse.quote(base64_data_str)


suanGetHost()
