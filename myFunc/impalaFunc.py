'''
Author: Logic
Date: 2022-04-20 14:25:56
LastEditTime: 2022-04-25 09:40:46
FilePath: \py_func_manage\myFunc\impalaFunc.py
Description: 
'''
import warnings

from impala.dbapi import connect

from .dbFunc import DbColumn, DbFunc
from .configFunc import getDict
from typing import List

'''
description:  impala连接接对象
param {*}
return {*}
'''


class Impala(DbFunc):
    __conn__ = None

    '''
    默认连接加密配置为不加密
    '''
    __auth_mechanism__ = 'PLAIN'

    def __init__(self,  config: dict):
        self.__conn__ = connect(host=config['host'],
                                port=int(config['port']),
                                user=config['user'],
                                password=config['pwd'],
                                database=config['db'],
                                auth_mechanism=self.__auth_mechanism__,
                                )

    def conn(self):
        return self.__conn__

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None

    def execQuery(self, sql: str):
        conn = self.conn()
        cur = conn.cursor(dictify=True)
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        return resList

    def tables(self) -> List[str]:
        return list(map(lambda x: x['name'], self.execQuery(' show tables ')))

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        sql = 'DESCRIBE ' + tbName
        dataList = self.execQuery(sql)
        return list(map(lambda x: DbColumn(x), dataList))

    def createSql(self, tbName: str) -> str:
        sql = " show create table  "+tbName
        return self.execQuery(sql)[0]['result']


def fixedImpala(ns: str = 'impala') -> Impala:
    return Impala(getDict(ns))
