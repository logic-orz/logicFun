from typing import List, Dict
from ..basic.exClass import BaseClass
from ..basic.configFunc import getDict
import abc
import datetime
from dataclasses import dataclass
from pydantic import BaseModel
from ..exFunc import *


class DbConfig(BaseModel, BaseClass):
    """
    数据库连接配置对象
    """
    host: str = None
    port: int = None
    user: str = None
    pwd: str = None
    db: str = None
    hosts: str = None


class DbColumn(BaseModel, BaseClass):
    """
    字段信息对象
    """
    name: str = None
    type: str = None
    comment: str = None
    primary_key: str = None
    default_value: str = None
    nullable: str = None


def transData(datas: List[Dict], colums: List[DbColumn], z2e: bool = True):
    """_summary_
    数据字段名转换
    @param z2e: True中文转英文(默认) False:英文转中文
    """
    for data in datas:
        for col in colums:
            if z2e:
                fkey = col.comment
                tKey = col.name
            else:
                fkey = col.name
                tKey = col.comment

            vType = col.type
            if fkey in data.keys():
                v = data.pop(fkey)
                if vType.startswith('float') and isinstance(v, str):
                    v = float(v)
                elif vType.startswith('int') and isinstance(v, str):
                    v = int(v)
                elif vType.startswith('double') and isinstance(v, str):
                    v = float(v)
                elif vType.startswith('decimal') and isinstance(v, str):
                    v = float(v)
                data[tKey] = v
    return datas


class DbFunc(metaclass=abc.ABCMeta):

    def __init__(self, config: DbConfig) -> None:
        pass

    @abc.abstractmethod
    def conn(self):
        # * 创建连接对象
        # TODO:子类实现
        raise Exception("子类实现创建连接对象方法")

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)

        if cur.rowcount > 0:
            res_list = cur.fetchall()
        else:
            res_list = []

        cur.close()
        return res_list

    def execQueryIte(self, sql: str, batchSize: int = 100):
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        i = 0
        while True:
            i += 1
            res_list = cur.fetchmany(batchSize)
            if not res_list:
                cur.close()
                return
            yield res_list

    def execQueryNoRes(self, *sqls: List[str]) -> None:
        self.execSqls(*sqls)

    def execSqls(self, *sqls: List[str]) -> None:
        conn = self.conn()
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)
        conn.commit()
        cur.close()

    def tables(self) -> List[str]:
        # * 获取所有数据表名
        # todo 子类实现
        raise Exception("方法未实现")

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        """
        * 获取表的字段模式
        todo 子类实现
        """
        raise Exception("方法未实现")

    @classmethod
    def fix(cls, ns: str = None):
        if not ns:
            ns = cls.__name__.lower()
        return cls(DbConfig.build(getDict(ns)))


def createInsertSql(tbName: str, *datas):

    keys = list(datas[0].keys())

    tmpValue = ''
    for data in datas:
        values = []
        for s in keys:
            if isinstance(data[s], str):
                vs = '"%s"' % (data[s].replace(
                    "\\", "\\\\").replace("\"", "\\\""))
            elif isinstance(data[s], datetime.datetime):
                vs = '"%s"' % (str(data[s]).replace("\"", "\\\""))
            elif not data[s]:
                vs = "null"
            else:
                vs = "%s" % (data[s])

            values.append(vs)

        tmpValue = tmpValue+"({values}),".format(values=','.join(values))

    fields = ', '.join(keys)
    valueStr = tmpValue[:-1]
    sql = f'INSERT INTO {tbName}({fields}) VALUES {valueStr}'
    return sql
