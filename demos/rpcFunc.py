import zerorpc
from zerorpc import Client
import queue


class ObjPool():
    def __init__(self, items):
        self._queue = queue.Queue(len(items))
        for item in items:
            self._queue.put(item)

    def get(self):
        return self._queue.get()

    def back(self, item):
        self._queue.put(item)

class BasicRpc(object):
    __objPool = []
    pass

def runRpcServer(basicRpc: BasicRpc, port: int = 1123):
    server = zerorpc.Server(basicRpc)
    server.bind("tcp://0.0.0.0:"+str(port))
    print('start rpc!')
    zerorpc.gevent.spawn(server.run)
    while True:
        zerorpc.gevent.sleep(2)
        # print('rpc is running!')

def loadRpcClient(ip: str = '127.0.0.1', port: int = 1123) -> Client:
    client = zerorpc.Client()
    client.connect("tcp://"+ip+":"+str(port))
    return client
