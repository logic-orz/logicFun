'''
Author: Logic
Date: 2022-04-20 14:36:14
LastEditTime: 2022-05-19 16:28:18
FilePath: \pyFuncs\cttqFuncs\conn\dbFunc.py
Description: 
'''
import json
from typing import List, Dict
from cttqFuncs.basic.exClass import BaseClass
import abc


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


class DbColumn(BaseClass):
    """
    字段信息对象
    """
    name: str = None
    type: str = None
    comment: str = None
    primary_key = None
    default_value = None
    nullable = None


class DbFunc(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def conn(self):
        # * 创建连接对象
        # TODO:子类实现
        raise Exception("子类实现创建连接对象方法")

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        res_list = cur.fetchall()

        cur.close()
        return res_list

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
