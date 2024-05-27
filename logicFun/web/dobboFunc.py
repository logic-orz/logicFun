from typing import List
import dubborequests
from dubborequests.config import Config


class DobboFunc():
    def __init__(self, servers: List[str], serverPath: str) -> None:
        Config.zookeeper_url_list = servers
        self.serverPath = serverPath
    # 获取dubbo服务详情

    def serverDetail(self):
        data = dubborequests.search(self.serverPath)
        print(data)

    # 获取dubbo服务下的所有方法
    def listFuncs(self):
        service_data = dubborequests.list(self.serverPath)
        print(service_data)

    # 获取dubbo服务指定的方法
    def getFunc(self, funcName: str):
        method_data = dubborequests.list(self.serverPath, funcName)
        print(method_data)

    def invokeFunc(self, funcName, data):
        res_data = dubborequests.zk_invoke(self.serverPath, funcName, data)
        print(res_data)
