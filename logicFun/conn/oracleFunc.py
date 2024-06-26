# python 连接 oracle 需要 加载三个dll驱动
from .dbFunc import DbFunc, DbColumn, DbConfig
from ..basic.configFunc import getDict
from typing import List
import cx_Oracle


class Oracle(DbFunc):
    def __init__(self, config: DbConfig):
        self.__conn__ = cx_Oracle.connect(
            config.user, config.pwd,
            config.host+':'+config.port+'/'+config.db
        )

    def conn(self):
        return self.__conn__

    def execQuery(self, *sqls: str):
        conn = self.conn()
        cur = conn.cursor()
        for sql in sqls:
            if sql.strip().endswith(";"):
                sql = sql.strip()[:-1]
            cur.execute(sql)
        cols = [d[0] for d in cur.description]
        resList = []
        for tup in cur.fetchall():
            resList.append(dict(zip(cols, tup)))

        cur.close()
        return resList

    def execQueryIte(self, sql: str, batchSize: int = 100, showStep: bool = False):
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        i = 0
        while True:
            i += 1
            if showStep:
                print("fetch batch ", i)

            resList = []
            for tup in cur.fetchmany(batchSize):
                resList.append(dict(zip(cols, tup)))
            if not resList:
                cur.close()
                return
            yield resList

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None
<<<<<<< HEAD:logicFun/conn/oracleFunc.py

=======
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/oracleFunc.py
