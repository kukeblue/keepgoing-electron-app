import compileall
import os
import time


path = r'F:\project\keepgoing-electron-app\main\electron\py\__pycache__'
file_names = os.listdir(path)  # 创建一个所有文件名的列表

for name in file_names:
    photo_name = str(name).split('.')[0]
    print(photo_name)
    if(photo_name != 'config' and photo_name != 'test_pics'):
        os.remove(os.path.join(path, name))

compileall.compile_dir('./py', force=True)

path = r'F:\project\keepgoing-electron-app\main\electron\py\__pycache__'
file_names = os.listdir(path)  # 创建一个所有文件名的列表

for name in file_names:
    photo_name = str(name).split('.')[0]
    if(photo_name != 'config' and photo_name != 'test_pics'):
        new_name = photo_name + '.pyc'
        os.rename(os.path.join(path, name), os.path.join(path, new_name))
