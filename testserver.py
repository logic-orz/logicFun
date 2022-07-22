import multiprocessing
import socket


class Server():
    def __init__(self, host: str = '127.0.0.1', port: int = 10086) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))                                      # 绑定地址
        self.s.listen(5)
        self.waitWorker()

    def waitWorker(self):
        def waiting(s):
            while True:
                print('wait')
                conn, addr = s.accept()                                       # 等待客户端连接
                print('欢迎{}'.format(addr))
                self.listen(conn)
        p = multiprocessing.Process(target=waiting(self.s))
        p.daemon = True
        p.start()

    def listen(self, conn):
       # 打印访问的用户信息
        def listening(conn):
            while True:
                print('talk')
                data = conn.recv(1024)
                dt = data.decode('utf-8')  # 接收一个1024字节的数据
                print(dt)
                conn.send('hello too'.encode('utf-8'))
                if dt == 'stop':
                    conn.send('ok'.encode('utf-8'))
                    conn.close()

        p = multiprocessing.Process(target=listening(conn))
        p.daemon = True
        p.start()


# def server(host: str = '127.0.0.1', port: int = 10086):
#     # 创建socket对象
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))                                      # 绑定地址
#     s.listen(5)                                               # 建立5个监听
#     while True:
#         conn, addr = s.accept()                                       # 等待客户端连接
#         print('欢迎{}'.format(addr))  # 打印访问的用户信息
#         while True:
#             data = conn.recv(1024)
#             dt = data.decode('utf-8')  # 接收一个1024字节的数据
#             print(dt)
#             if dt == 'stop':
#                 conn.send('hello'.encode('utf-8'))
#                 conn.close()


Server()
