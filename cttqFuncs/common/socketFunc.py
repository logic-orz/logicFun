import os
from multiprocessing.reduction import recv_handle
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from multiprocessing.reduction import send_handle
import socket


class SocketServer():
    """
    * 通信服务端
    """

    def __init__(self, work_addr, port, authkey = b'default'):
        # 等待工作者进程接入
        work_serv = Listener(work_addr, authkey=authkey)
        worker = work_serv.accept()  # 接收工作者进程
        work_pid = worker.recv()  # 接收工作者进程pid

        # 等待TCP/IP客户端接入，并且将客户端实例发送给工作者进程
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.bind(('', port))
        s.listen(1)
        while True:
            client, addr = s.accept()
            print('SERVER GOT CLIENT:', addr)
            send_handle(worker, client.fileno(), work_pid)
            client.close()


class SocketWorker():
    """
    * 通信应用端
    """

    def __init__(self, server_address, authkey = b'default'):
        # 向服务器进程注册，指明参加的是哪一个服务器进程
        serv = Client(server_address, authkey=authkey)
        serv.send(os.getpid())  # 向服务器进程发送自己的进程id
        while True:
            fd = recv_handle()  # 接收服务器进程发来的用户套接字的文件描述符
            print('got a client fileno:', fd)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                while True:
                    msg = s.recv(1024)
                    if not msg:
                        break
                    print('worker recived a message:{0!r}'.format(msg))
                    s.send(msg)


if __name__ == '__main__':
    # import concurrent.futures as cf
    # pool=cf.ProcessPoolExecutor(max_workers=8)
    # pool.submit(SocketServer("127.0.0.1",8765))
    # pool.submit(SocketWorker("127.0.0.1:8765"))
    SocketServer("127.0.0.1",8765)