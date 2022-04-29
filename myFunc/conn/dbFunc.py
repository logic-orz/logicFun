'''
Author: Logic
Date: 2022-04-20 14:36:14
LastEditTime: 2022-04-29 11:21:08
FilePath: \pyFuncs\myFunc\conn\dbFunc.py
Description: 
'''
import json
from typing import List, overload
from myFunc.basic.configFunc import getDict
from myFunc.basic.myClass import BaseClass
from typing import Dict


class DbConfig(BaseClass):
    """
    数据库连接配置对象
    """

    def __init__(self) -> None:
        self.host: str = None
        self.port: str = None
        self.user: str = None
        self.pwd: str = None
        self.db: str = None
        self.hosts: str = None


class DbColumn(BaseClass):
    """
    字段信息对象
    """

    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None


class DbFunc:

    def conn(self):
        # * 创建连接对象
        # TODO:子类实现
        pass

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        res_list = cur.fetchall()

        cur.close()
        return res_list

    def execQueryNoRes(self, sql: str) -> None:
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()

    def tables(self) -> List[str]:
        # * 获取所有数据表名
        # todo 子类实现
        pass

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        """
        * 获取表的字段模式
        todo 子类实现
        """
        pass
