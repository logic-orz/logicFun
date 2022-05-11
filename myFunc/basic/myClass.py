'''
Author: Logic
Date: 2022-04-26 08:55:29
LastEditTime: 2022-05-09 17:08:24
FilePath: \pyFuncs\myFunc\basic\myClass.py
Description:
'''
import json
from typing import TypeVar, Generic, Dict, List, Set, Tuple
from .signFunc import *


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

    def toStr(self):
        return ''.join(self.__strList__)




class Tree(Generic[T]):

    """
    * data:Dict[str:Tuple[str,T]] 对象字典:[key,[parentKey,value]]
    * path:Dict[str:set[str]] 路径层级关系
    """

    def __init__(self, name: str = '') -> None:
        self.name = name
        self.data: Dict[str, Tuple[str, T]] = dict()
        self.child: Dict[str, Set[str]] = dict()

    def add(self, key: str, v: T, parentKey: str = None):
        self.data[key] = (parentKey, v)

        children = set()
        if parentKey in self.child:
            children = self.child[parentKey]

        children.add(key)
        self.child[parentKey] = children

    def get(self, key: str) -> T:
        if key in self.data:
            return self.data[key][1]
        return None

    def delete(self, key: str):
        childKeys = {key}

        tmpkeys: List[str] = [key]
        

        while len(tmpkeys) > 0:
            ts = []
            for tmp in tmpkeys :
                ts.appendAll(self.getChildrenKeys(tmp))

            tmpkeys.clear()
            tmpkeys.appendAll(ts)

        pk = self.data[key][0]
        ps = self.child[pk]
        ps.remove(key)
        if len(ps) == 0:
            del self.child[pk]
        for k in childKeys:
            del self.child[k]
            del self.data[k]

    def getChildren(self, key: str) -> List[T]:
        if key in self.child:
            return self.child[key].toList().map(lambda k: self.data[k][1])
        return []

    def getChildrenKeys(self, key: str) -> List[str]:
        if key in self.child:
            return self.child[key].toList()
        return []

    def getParent(self, key: str) -> T:
        if key in self.data:
            pk = self.data[key][0]
            return self.data[pk][1]
        return None
