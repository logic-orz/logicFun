from impala.dbapi import connect
from .dbFunc import DbColumn, DbConfig, DbFunc
from typing import List
from ..exFunc import *
<<<<<<< HEAD:logicFun/conn/impalaFunc.py
=======
from impala.hiveserver2 import HiveServer2Connection

>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/impalaFunc.py

class Impala(DbFunc):

    '''
    默认连接加密配置为不加密
    '''
    __auth_mechanism__ = 'PLAIN'
    __config_ns__= 'impala'

    def __init__(self, config: DbConfig):
        self.config: DbConfig = config
        self.__conn__: HiveServer2Connection = connect(host=config.host,
                                                       port=int(config.port),
                                                       user=config.user,
                                                       password=config.pwd,
                                                       database=config.db,
                                                       auth_mechanism=self.__auth_mechanism__,
                                                       )

    def conn(self):
        return self.__conn__

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None

    def execQuery(self, *sqls):
        conn = self.conn()
        cur = conn.cursor(dictify=True)
        for sql in sqls:
            cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        return resList

    def execQueryIte(self, *sqls: str, batchSize: int = 100, showStep: bool = False):
        conn = self.conn()
        cur = conn.cursor(dictify=True)
        for sql in sqls:
            cur.execute(sql)
        i = 0
        while True:
            i += 1
            if showStep:
                print("fetch batch ", i)
            res_list = cur.fetchmany(batchSize)
            if not res_list:
                cur.close()
                return
            yield res_list

    def tables(self) -> List[str]:
        return self.execQuery(' show tables ').map(lambda x: x['name'])

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        sql = 'DESCRIBE ' + tbName
        
        res:List[DbColumn]=[]
        datas=self.execQuery(sql)
        for x in datas:
            dc=DbColumn(name=x['name'],type=x['type'],comment=x['comment'])
            if 'primary_key' in x:
                dc.isId= bool(x['primary_key'])
                
            res.append(dc)
        return res

    def createSql(self, tbName: str) -> str:
        sql = " show create table  " + tbName
        return self.execQuery(sql)[0]['result']
