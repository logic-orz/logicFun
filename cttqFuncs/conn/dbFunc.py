import json
from typing import List, Dict
from ..basic.exClass import BaseClass
from ..basic.configFunc import getDict
import abc
import datetime
from dataclasses import dataclass

@dataclass(init=False)
class DbConfig(BaseClass):
    """
    数据库连接配置对象
    """
    host: str = None
    port: int = None
    user: str = None
    pwd: str = None
    db: str = None
    hosts: str = None

@dataclass(init=False)
class DbColumn(BaseClass):
    """
    字段信息对象
    """
    name: str = None
    type: str = None
    comment: str = None
    primary_key:str = None
    default_value:str = None
    nullable:str = None


class DbFunc(metaclass=abc.ABCMeta):
    
    def __init__(self,config: DbConfig) -> None:
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

    def execQueryIte(self, sql: str, batchSize: int = 100, showStep: bool = False):
        conn = self.conn()
        cur = conn.cursor()
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

    def execQueryNoRes(self, *sqls) -> None:
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
    def fix(cls,ns:str=None):
        if not ns:
            ns=cls.__name__.lower()
        return cls(DbConfig.build(getDict(ns)))


# def createInsertSql(tbName: str, data: Dict):

#     keys = list(data.keys())
#     values = []
#     for s in keys:
#         if isinstance(data[s], str):
#             values.append('"%s"' % (data[s].replace("\\","\\\\").replace("\"", "\\\"")))
#         elif isinstance(data[s], datetime.datetime):
#             values.append('"%s"' % (str(data[s]).replace("\"", "\\\"")))
#         elif not data[s]:
#             values.append("null")
#         else:
#             values.append("%s" % (data[s]))

#     sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(
#         table=tbName, keys=', '.join(keys), values=', '.join(values))
#     return sql


def createInsertSql(tbName: str, *datas):

    keys = list(datas[0].keys())

    tmpValue = ''
    for data in datas:
        values = []
        for s in keys:
            
            if isinstance(data[s], str):
                vs='"%s"' % (data[s].replace("\\","\\\\").replace("\"", "\\\""))
                # values.append('"%s"' % (data[s].replace("\\","\\\\").replace("\"", "\\\"")))
            elif isinstance(data[s], datetime.datetime):
                vs='"%s"' % (str(data[s]).replace("\"", "\\\""))
                # values.append('"%s"' % (str(data[s]).replace("\"", "\\\"")))
            elif not data[s]:
                vs="null"
                # values.append("null")
            else:
                vs="%s" % (data[s])
                
            values.append(vs)
            
        tmpValue = tmpValue+"({values}),".format(values=','.join(values))
    
    fields=', '.join(keys)
    valueStr=tmpValue[:-1]
    sql = f'INSERT INTO {tbName}({fields}) VALUES {valueStr}'
    return sql
