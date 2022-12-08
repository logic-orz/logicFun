'''
Author: Logic
Date: 2022-04-20 14:27:40
LastEditTime: 2022-05-19 14:46:19
Description: 
'''
from typing import List
import pymysql
from pymysql import connect
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from .dbFunc import DbFunc, DbColumn, DbConfig
from ..basic.configFunc import getDict


class MysqlPool(DbFunc):

    def __init__(self, config: DbConfig):
        self.__pool__ = PooledDB(pymysql,
                                 10,
                                 host=config.host,
                                 user=config.user,
                                 passwd=config.pwd,
                                 db=config.db,
                                 port=int(config.port),
                                 charset="utf8",
                                 cursorclass=DictCursor
                                 )

    def conn(self):
        return self.__pool__.connection()

    def close(self):
        if self.__pool__ is not None:
            self.__pool__.close()
            self.__pool__ = None

    @staticmethod
    def fixedMysqlPool(ns: str = 'mysql'):
        return MysqlPool(DbConfig().build(getDict(ns)))


class Mysql(DbFunc):

    def __init__(self, config: DbConfig):
        self.__conn__ = connect(host=config.host,
                                port=int(config.port),
                                user=config.user,
                                password=config.pwd,
                                database=config.db,
                                charset="utf8",
                                cursorclass=DictCursor)

    def conn(self):
        self.__conn__.ping(reconnect=True)
        return self.__conn__

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None


    @staticmethod
    def fixedMysql(ns: str = 'mysql'):
        return Mysql(DbConfig().build(getDict(ns)))
