import requests
import zipfile
import tempfile

updateHome = __file__.strip('mhUpdate.py')


def get_data():
    url = "http://kuke-static.kukechen.top/py.zip"
    response = requests.get(url)
    return url, response.content


if __name__ == '__main__':
    url, data = get_data()  # data为byte字节

    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
    print(_tmp_file)

    _tmp_file.write(data)  # byte字节数据写入临时文件
    # _tmp_file.seek(0)

    zf = zipfile.ZipFile(_tmp_file, mode='r')
    for names in zf.namelist():
        f = zf.extract(names, updateHome)  # 解压到zip目录文件下
        print(f)

    zf.close()
