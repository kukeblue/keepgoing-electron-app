import socket
import time

if __name__ == '__main__':

    # 1 创建客户端套接字对象tcp_client_1
    # 参数介绍：AF_INET 代表IPV4类型, SOCK_STREAM代表tcp传输协议类型 ,注：AF_INET6代表IPV6

    tcp_client_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 2 通过客户端套接字的connect方法与服务器套接字建立连接
    # 参数介绍：前面的ip地址代表服务器的ip地址，后面的61234代表服务端的端口号 。
    tcp_client_1.connect(("127.0.0.1", 61234))
    while True:
        time.sleep(1)
        send_data = "rigthClick".encode(encoding='utf-8')
        tcp_client_1.send(send_data)
        recv_data = tcp_client_1.recv(1024)
        print(recv_data.decode(encoding='utf-8'))
