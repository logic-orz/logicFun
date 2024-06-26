import psycopg2
import psycopg2.extras

from ..basic.configFunc import getDict
from .dbFunc import DbColumn, DbConfig, DbFunc


class PostGres(DbFunc):

    def __init__(self, config: DbConfig):
        self.__conn__ = psycopg2.connect(host=config.host,
                                         port=int(config.port),
                                         user=config.user,
                                         password=config.pwd,
                                         database=config.db)

    def conn(self):
        return self.__conn__

    def execQuery(self, *sqls):
        conn = self.conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for sql in sqls:
            cur.execute(sql)
        resList = list(map(lambda row: dict(row), cur.fetchall()))
        cur.close()
        return resList

    def close(self):
        if self.__conn__ is not None:
            self.__conn__.close()
            self.__conn__ = None
<<<<<<< HEAD:logicFun/conn/postgresFunc.py

=======
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/conn/postgresFunc.py
