'''
pip install python-consul
'''

from dataclasses import dataclass
from typing import List

import consul

from ..exFunc import *
from ..basic.configFunc import getDict
from ..basic.exClass import BaseClass


class ServiceInfo(BaseClass):
    def __init__(self,data:dict) -> None:
        self.id= data['ID']
        self.name=data["Service"]
        self.tags=data['Tags']
        self.meta=data["Meta"]
        self.port=data["Port"]
        self.address=data["Address"]
        self.dataCenter=data["Datacenter"]


@dataclass(init=False)
class ConsulFunc(BaseClass):
    consul_ip: str = None
    consul_port: int = 8500
    local_ip: str = None
    service_id: str=None
    service_name: str = None
    local_port: int = None
    token: str = None

    def fixConfig(self, ns: str = 'consul'):
        self.build(getDict(ns))
        return self

    def init(self):
        # 初始化 Consul 服务
        self.cons = consul.Consul(host=self.consul_ip, port=8500)

    def register(self):
        # 注册服务到 Consul
        self.cons.agent.service.register(
            service_id=self.service_id if self.service_id else self.service_name,
            name=self.service_name,
            address=self.local_ip,
            port=self.local_port,
            token=self.token,
            # 心跳检查：间隔：5s，超时：30s，注销：30s
            check=consul.Check().tcp(self.local_ip, self.local_port, '5s', '30s', '60s'),
            tags=[]
        )

    def getService(self, name:str=None)->List[ServiceInfo]:
        services = self.cons.agent.services()
        sis=[]
        for id,service in services.kvs():
            si=ServiceInfo(service)
            sis.append(si)
            
        if name:
            sis=sis.filter(lambda si:si.name == name)
            
        return sis
