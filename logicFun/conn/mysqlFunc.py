from typing import List
import pymysql
from pymysql import connect
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from cttqFuncs.conn.dbFunc import DbFunc, DbColumn, DbConfig
from cttqFuncs.basic.configFunc import getDict


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
        self._conn = connect(host=config.host,
                                port=int(config.port),
                                user=config.user,
                                password=config.pwd,
                                database=config.db,
                                charset="utf8",
                                cursorclass=DictCursor)

    def conn(self):
        self._conn.ping(reconnect=True)
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

