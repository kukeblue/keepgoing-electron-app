#encoding=UTF-8

import sys
import os
import string
import win32com					#要下载对应的扩展程序,不明白的话，百度一下
import win32com.client				#要下载对应的扩展程序,不明白的话，百度一下
import pythoncom
import time
from ctypes import *
from win32com.client import Dispatch


#osapi_dll = windll.LoadLibrary('OLE32')
#osapi_dll.CoUninitialize()
#osapi_dll.CoInitializeEx(0,0)

#注册好爱插件
a=os.system('regsvr32 haoi.dll')
if a:
	print("注册 haoi.dll 成功!")
else:
	print("注册 haoi.dll 失败!")


	
haoi = Dispatch('haoi.dt')


# soft_key = '1001|9A42B0F1BD994C75'											# 软件Key，用于设置作者返利
# haoi.SetRebate(soft_key)													# 设置返利


# pic_file_path = os.path.join(os.path.dirname(__file__), 'test_pics', 'test1.jpg')

# #此处指的当前路径下的test_pics文件夹下面的test.jpg
# #可以修改成你想要的文件路径


# reply=haoi.SendFileEx('密码串','1001',pic_file_path,int(60),int(1),int(20),'',int(0),'beizhu')
# TID=haoi.TID #获取题目流水号，用于申诉错题

# if haoi.IsRight(reply): #判断是否为正常的答案格式
	
# 	print("返回的答案是:%s " % str(ret_id))
#     #输入内容提交 并判断验证码是否正确
#     #如果错误应调用SendError
#     #haoi.SendError(TID)  提交错误题目，进行申诉
#     #后再重新发送
# else:
# 	print("错误")
# 	# 应该延迟1秒后 重新截图 再重新发送
	

# raw_input('按任意键退出')