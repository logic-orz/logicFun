'''
Author: Logic
Date: 2022-04-26 08:55:29
LastEditTime: 2022-04-28 19:00:28
FilePath: \pyFuncs\myFunc\basic\myClass.py
Description:
'''
import json
from textwrap import wrap
from typing import TypeVar, Generic, Dict, List, Set, Tuple, overload
from .signFunc import *



# def builder(fun):  # * 基础方法装饰器
#     class wrapper():
#         def __init__(self):
#             self.wrapper = fun()  # * 保留一个original_class类对象

#         def build(self, _obj: Dict):
#             if _obj:
#                 self.__dict__.update(_obj)
#             return self

#         def toDict(self):
#             dict = {}
#             dict.update(self.__dict__)
#             if "_sa_instance_state" in dict:
#                 del dict['_sa_instance_state']
#             return dict

#         def __repr__(self) -> str:
#             return json.dumps(self.toDict(), ensure_ascii=False)

#     return wrapper


class BaseClass:

    def build(self, _obj: Dict):
        if _obj:
            self.__dict__.update(_obj)
        return self

    def toDict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']

        return dict

    def __repr__(self) -> str:
        return json.dumps(self.toDict(), ensure_ascii=False)


T = TypeVar('T')


class IndexList(Generic[T]):  # * 索引集合
    def __init__(self) -> None:

        self.numKey = 0  # * 递增key
        self.data: Dict[int, Tuple[T, List[str]]] = dict()
        self.index: Dict[str, Set[int]] = dict()

    def getNumKey(self):
        self.numKey += 1
        return self.numKey

    def add(self, t: T, keys: List[str]):

        num = self.getNumKey()
        self.data[num] = (t, keys)

        for key in keys:
            indexV = set()
            if key in self.index:
                indexV = self.index[key]
            indexV.add(num)
            self.index[key] = indexV

    def search(self, key: str) -> List[Tuple[int, T]]:
        if key in self.index:
            numSet = self.index[key]
            return numSet.toList()\
                .map(lambda n: (n, self.data[n][0]))
        return list()

    def remove(self, num: int):
        if not num in self.data:
            return

        tup = self.data[num]
        t = tup[0]
        keys = tup[1]

        del self.data[num]

        for key in keys:
            if not key in self.index:
                continue
            numSet = self.index[key]
            numSet.remove(num)
            if len(numSet) == 0:
                del self.index[key]
            else:
                self.index[key] = numSet

    def vs(self):
        return self.data.vs().map(lambda t: t[0])


class StrBuild():  # * 面向长字符串多次需要拼接的场景

    def __init__(self) -> None:
        self.__strList__ = []

    def append(self, s):
        self.__strList__.append(str(s))
        return self

    @property
    def toStr(self):
        return ''.join(self.__strList__)
