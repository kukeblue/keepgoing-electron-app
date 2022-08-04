# # encoding=UTF-8

# import sys
# import os
# import string
# import win32com.client  # 要下载对应的扩展程序,不明白的话，百度一下
# import pythoncom
# import time
# import win32api
# import win32con
# from ctypes import *
# from win32com.client import Dispatch
# import baiduApi


# hwnds = baiduApi.op.EnumWindow(0,"记事本","",1+4+8+16)
# print(hwnds)
# ret = baiduApi.op.BindWindow(hwnds, "normal", "windows", "windows", 1);
# print(ret)
# baiduApi.op.MoveTo(100, 200)
# baiduApi.op.LeftClick()
# time.sleep(1)
# win32api.SetCursorPos([30,150])
# win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
# cx = 1009
# cy = 100
# long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
# win32api.SendMessage(hwnds, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
# win32api.SendMessage(hwnds, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起
# baiduApi.op.KeyPressChar('9')

# hwnds = split(hwnds,",")

# txt_hwnd=baiduApi.op.FindWindow("","新建文本文档.txt - 记事本")
# print(txt_hwnd)
# print(baiduApi.op.GetWindowProcessPath(txt_hwnd))
# print(baiduApi.op.SetWindowState(txt_hwnd,4))
#osapi_dll = windll.LoadLibrary('OLE32')
# osapi_dll.CoUninitialize()
# osapi_dll.CoInitializeEx(0,0)

# 注册好爱插件
# a=os.system('regsvr32 haoi.dll')
# if a:
# 	print("注册 haoi.dll 成功!")
# else:
# 	print("注册 haoi.dll 失败!")


# haoi = Dispatch('haoi.dt')


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
import mouse
# raw_input('按任意键退出')

mouse.move("100", "100", duration=0.4, absolute=True)
