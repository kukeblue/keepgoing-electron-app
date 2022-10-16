import compileall
import os
compileall.compile_dir('./py', force=True)

path = r'D:\project\keepgoing-electron-app\main\electron\py\__pycache__'
file_names = os.listdir(path)  # 创建一个所有文件名的列表

i = 1
for name in file_names:
    photo_name = str(name).split('.')[0]
    new_name = photo_name + '.pyc'
    os.rename(os.path.join(path, name), os.path.join(path, new_name))
