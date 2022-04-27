'''
Author: Logic
Date: 2022-04-20 14:36:14
LastEditTime: 2022-04-21 14:33:17
FilePath: \py_func_manage\myFunc\dbFunc.py
Description: 
'''
import json
from typing import List


class DbColumn:

    def __init__(self, data: dict):
        self.name = data['name']
        self.type = data['type']
        self.comment = data['comment']

    def __repr__(self) -> str:
        return json.dumps(obj=self.__dict__, ensure_ascii=False)


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

    def tables(self)-> List[str]:
        # * 获取所有数据表名
        # todo 子类实现
        pass

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        """
        * 获取表的字段模式
        todo 子类实现
        """
        pass
