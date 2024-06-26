<<<<<<< HEAD:logicFun/conn/mysqlFunc.py
from typing import List
=======
from typing import Dict, List

import aiomysql
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/mysqlFunc.py
import pymysql
from aiomysql.pool import Pool
from dbutils.pooled_db import PooledDB
from pymysql import connect
from pymysql.cursors import DictCursor

from ..basic.configFunc import getDict
from .dbFunc import DbConfig, DbFunc, DbColumn


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

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.raw = True
        cur.execute(sql)

        if cur.rowcount > 0:
            res_list = cur.fetchall()
        else:
            res_list = []

        cur.close()
        return res_list

    def execQueryIte(self, *sqls: str, batchSize: int = 1000):
        conn = self.conn()
        cur = conn.cursor()
        cur.raw = True
        for sql in sqls:
            cur.execute(sql)
        i = 0
        while True:
            i += 1
            res_list = cur.fetchmany(batchSize)
            if not res_list:
                cur.close()
                return
            yield res_list

    def close(self):
        if self.__pool__ is not None:
            self.__pool__.close()
            self.__pool__ = None

    @staticmethod
    def fixedMysqlPool(ns: str = 'mysql'):
        return MysqlPool(DbConfig().build(getDict(ns)))


class MysqlPoolAsync:

    def __init__(self, config: DbConfig, loop=None):
        self.config = config
        self.loop = loop
        self.pool: Pool = None

    async def __initPool(self):
        self.pool = await aiomysql.create_pool(
            host=self.config.host,
            user=self.config.user,
            password=self.config.pwd,
            db=self.config.db,
            port=int(self.config.port),
            charset="utf8",
            cursorclass=aiomysql.DictCursor,
            autocommit=True,
            loop=self.loop
        )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execQuery(self, *sqls: str) -> List[dict]:
        if not self.pool:
            await self.__initPool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                for sql in sqls:
                    await cur.execute(sql)
                if cur.rowcount > 0:
                    res_list = await cur.fetchall()
                else:
                    res_list = []

                return res_list

    async def execQueryIte(self, *sqls: str, batchSize: int = 100):
        if not self.pool:
            await self.__initPool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                for sql in sqls:
                    await cur.execute(sql)
                while True:
                    res_list = cur.fetchmany(batchSize)
                    if not res_list:
                        return
                    yield res_list

    async def execSql(self, *sqls: str) -> None:
        if not self.pool:
            await self.__initPool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                for sql in sqls:
                    await cur.execute(sql)

    async def tableMeta(self, tbName: str) -> List[DbColumn]:
        sql = f"show full columns from {tbName} "
        datas: List[Dict] = await self.execQuery(sql)
        cols: List[DbColumn] = datas.map(lambda d: DbColumn(name=d['Field'], comment=d['Comment'], type=d['Type'], isId=(d['Key'] == 'PRI')))
        return cols

    @staticmethod
    def fix(ns: str = 'mysql'):
        return MysqlPoolAsync(DbConfig().build(getDict(ns)))


class Mysql(DbFunc):

    def __init__(self, config: DbConfig):
        self._conn = connect(host=config.host,
<<<<<<< HEAD:logicFun/conn/mysqlFunc.py
                                port=int(config.port),
                                user=config.user,
                                password=config.pwd,
                                database=config.db,
                                charset="utf8",
                                cursorclass=DictCursor)
=======
                             port=int(config.port),
                             user=config.user,
                             password=config.pwd,
                             database=config.db,
                             charset="utf8",
                             cursorclass=DictCursor)

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.raw = True
        cur.execute(sql)

        if cur.rowcount > 0:
            res_list = cur.fetchall()
        else:
            res_list = []

        cur.close()
        return res_list

    def execQueryIte(self, *sqls: str, batchSize: int = 1000):
        conn = self.conn()
        cur = conn.cursor()
        cur.raw = True
        for sql in sqls:
            cur.execute(sql)
        i = 0
        while True:
            i += 1
            res_list = cur.fetchmany(batchSize)
            if not res_list:
                cur.close()
                return
            yield res_list
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/mysqlFunc.py

    def conn(self):
        self._conn.ping(reconnect=True)
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

<<<<<<< HEAD:logicFun/conn/mysqlFunc.py
=======
    def tableMeta(self, tbName: str) -> List[DbColumn]:
        sql = f"show full columns from {tbName} "
        datas: List[Dict] = self.execQuery(sql)
        cols: List[DbColumn] = datas.map(lambda d: DbColumn(name=d['Field'], comment=d['Comment'], type=d['Type'], isId=(d['Key'] == 'PRI')))
        return cols
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/mysqlFunc.py
