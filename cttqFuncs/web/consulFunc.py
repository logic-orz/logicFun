'''
pip install python-consul
'''

from typing import List

import consul

from ..exFunc import *
from ..basic.configFunc import getDict
from ..basic.exClass import BaseClass
from ..basic.configFunc import initStr

class ServiceInfo(BaseClass):
    def __init__(self,data:dict) -> None:
        self.id= data['ID']
        self.name=data["Service"]
        self.tags=data['Tags']
        self.meta=data["Meta"]
        self.port=data["Port"]
        self.address=data["Address"]
        self.dataCenter=data["Datacenter"]


class ConsulFunc(BaseClass):
  
    def __init__(self,consulIp:str='127.0.0.1',consulPort:int=8500) -> None:
        
        self.consulIp = consulIp
        self.consulPort = consulPort
        
        self.local_ip: str = '127.0.0.1'
        self.local_port: int = None
        
        self.service_id: str=None
        self.service_name: str = None
        
        self.token: str = None
        self.cons=None

    def fix(self, ns: str = 'consul'):
        self.build(getDict(ns))
        return self

    def _connect(self):
        # 初始化 Consul 服务
        self.cons = consul.Consul(host=self.consulIp, port=self.consulPort)

    def register(self):
        if self.cons is None:
            self._connect()
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
    def deRegister(self):
        self.cons.agent.service.deregister(service_id=self.service_id if self.service_id else self.service_name)
    
    def getKV(self,key:str):
        if self.cons is None:
            self._connect()
            
        kv=self.cons.kv.get(key)
        if not kv:
            return None
        v=kv[1]['Value']
        v= str(v, encoding = "utf-8")
        return v
    
    def syncConfig(self,key:str):
        initStr(self.getKV(key))
        
    
    def getService(self, name:str=None)->List[ServiceInfo]:
        if self.cons is None:
            self._connect()
            
        services = self.cons.agent.services()
        sis=[]
        for id,service in services.kvs():
            si=ServiceInfo(service)
            sis.append(si)
            
        if name:
            sis=sis.filter(lambda si:si.name == name)
            
        return sis

