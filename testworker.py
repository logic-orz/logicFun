import socket
import sys


class Worker():
    def __init__(self, host: str = '127.0.0.1', port: int = 10086) -> None:
        self.c = socket.socket()                                           # 创建socket对象
        self.c.connect((host, port))  # 建立连接

    def send(self, msg: str) -> str:
        self.c.send(msg.encode('utf-8'))  # 发送数据
        data = self.c.recv(1024)  # 接收一个1024字节的数据
        print('收到：', data.decode('utf-8'))
        return data

    def close(self):
        self.c.send('stop'.encode('utf-8'))
        self.c.close()


w = Worker()
w.send("hello")
w.close()
