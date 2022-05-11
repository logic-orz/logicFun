'''
Author: Logic
Date: 2022-04-20 14:27:40
LastEditTime: 2022-05-09 15:07:18
FilePath: \pyFuncs\myFunc\conn\mysqlFunc.py
Description: 
'''
import pymysql
from pymysql import connect
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB
from myFunc.conn.dbFunc import DbFunc, DbColumn, DbConfig


from urllib.parse import quote_plus as urlquote
from myFunc.basic.configFunc import getDict


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
        return self.__conn__

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None

    @staticmethod
    def fixedMysql(ns: str = 'mysql'):
        return Mysql(DbConfig().build(getDict(ns)))

    @staticmethod
    def fixedEngine(ns: str = 'mysql', isFlask: bool = False):

        config = DbConfig().build(getDict(ns))

        DB_CONNECT = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
            config.user, urlquote(config.pwd), config.host, config.port, config.db)

        if isFlask:
            from flask_sqlalchemy import create_engine
        else:
            from sqlalchemy import create_engine

        engine = create_engine(
            DB_CONNECT,
            max_overflow=5,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            pool_pre_ping=True,
        )
        return engine
