'''
Author: Logic
Date: 2022-04-20 14:25:56
LastEditTime: 2022-04-29 10:50:20
FilePath: \pyFuncs\myFunc\conn\impalaFunc.py
Description: 
'''
import warnings

from impala.dbapi import connect

from .dbFunc import DbColumn, DbConfig, DbFunc
from ..basic.configFunc import getDict
from typing import List

'''
description:  impala连接接对象
param {*}
return {*}
'''


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

    def execQuery(self, sql: str):
        conn = self.conn()
        cur = conn.cursor(dictify=True)
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        return resList

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