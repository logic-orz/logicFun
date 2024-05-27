import json
import socket
import threading
import time
import struct
 
class Server():
    def __init__(self):
        self.g_conn_pool = {}  # 连接池
        # 记录客户端数量
        self.num =0
        # 服务器本地地址
        self.address = ('0.0.0.0', 8000)
        # 初始化服务器
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(128)
        
    def accept_client(self):
        """
            接收新连接
            """
        while True:
            client_socket, info = self.server_socket.accept()  # 阻塞，等待客户端连接
            print(client_socket,info)
            # 给每个客户端创建一个独立的线程进行管理
            thread = threading.Thread(target=self.recv_msg, args=(client_socket,info))
            thread.setDaemon(True)
            thread.start()
            
    def recv_msg(self,client,info):
        # 提示服务器开启成功
        print('服务器已准备就绪！')
        client.sendall("connect server successfully!".encode(encoding='utf8'))
        # 持续接受客户端连接
        while True:
            try:
                client.sendall(b'Success')
                while True:
                    msg = client.recv(1024)
                    msg_recv = msg.decode('utf-8')
                    if not msg_recv:
                        continue
                    else:
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print('客户端 ' + recv_time + ':\n')
                        print(' ' + msg_recv + '\n')
            except Exception as e:
 
                print('客户端断开连接...')
                exit(-1)
                break
    def start_new_thread(self):
        """启动新线程来接收信息"""
        thread = threading.Thread(target=self.accept_client, args=())
        thread.setDaemon(True)
        thread.start()


class Client():
 
    def __init__(self):
     #服务器ip与端口
        self.server_address = ('127.0.0.1', 8000)
         
        self.num = 0
    def recv_msg(self):
        print("正在连接服务器....")
 
        # 客户端连接服务器
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #连接服务器
                self.client_socket.connect(self.server_address)
 
                num = self.num
 
                # 制作报头
                header_dic = {
                    'filename': num
                }
                header_bytes = json.dumps(header_dic).encode('utf-8')
                self.client_socket.send(struct.pack('i', len(header_bytes)))
                self.client_socket.send(header_bytes)
                 
    #接收信息
                while True:
                    msg_recv = self.client_socket.recv(1024).decode('gbk')
                    print(msg_recv)
 
                    if msg_recv == 'Success':
                        print('客户端已与服务器成功建立连接...')
                    elif not msg_recv:
                        continue
                    else:
                        recv_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        print( '服务器 ' + recv_time + ':\n')
                        print(' ' + msg_recv + '\n')
 
            except:
                print('与服务器断开连接...')
                break
    def start_new_thread(self):
        """启动新线程来接收信息"""
        thread = threading.Thread(target=self.recv_msg, args=())
        thread.setDaemon(True)
        thread.start()