'''
Author: Logic
Date: 2022-04-20 14:25:56
LastEditTime: 2022-05-19 16:32:18
Description: 
'''

from impala.dbapi import connect
from .dbFunc import DbColumn, DbConfig, DbFunc
from ..basic.configFunc import getDict
from typing import List
from ..basic.exFunc import *

class Impala(DbFunc):

    '''
    默认连接加密配置为不加密
    '''
    __auth_mechanism__ = 'PLAIN'

    def __init__(self,  config: DbConfig):
        self.__conn__ = connect(host=config.host,
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

    def execQueryIte(self, sql: str, batchSize: int = 100, showStep: bool = False):
        conn = self.conn()
        cur = conn.cursor(dictify=True)
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
        return self.execQuery(sql).map(lambda x: DbColumn().build(x))

    def createSql(self, tbName: str) -> str:
        sql = " show create table  "+tbName
        return self.execQuery(sql)[0]['result']

    @staticmethod
    def fixedImpala(ns: str = 'impala'):
        return Impala(DbConfig().build(getDict(ns)))
