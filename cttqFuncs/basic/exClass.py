'''
Author: Logic
Date: 2022-04-26 08:55:29
Description:
'''
import datetime
import json
from typing import Dict, Generic, List, Set, Tuple, TypeVar

T = TypeVar('T')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # 检查到是bytes类型的数据就转为str类型
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        # 检查到是datetime.datetime类型的数据就转为str类型
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, BaseClass):
            return obj.toDict()
        return json.JSONEncoder.default(self, obj)


class CommonException(Exception):
    def __init__(self, ErrorInfo):
        self.ErrorInfo = ErrorInfo

    def __str__(self):
        return self.ErrorInfo


class BaseClass:

    """
    * 基础父类,提供面向dict的转换方法
    """

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

    def toStr(self):
        return json.dumps(self.toDict(), cls=MyEncoder, ensure_ascii=False, indent=2)

    def __str__(self):
        return json.dumps(self.toDict(),  cls=MyEncoder, ensure_ascii=False, indent=2)

    def __repr__(self) -> str:
        return json.dumps(self.toDict(),  cls=MyEncoder, ensure_ascii=False, indent=2)


class IndexList(Generic[T]):
    """
     * 索引集合,主要面向检索，不建议修改数据
    """

    def __init__(self) -> None:
        self.data: List[Tuple[T, List[str]]] = list()
        self.index: Dict[str, Set[int]] = dict()

    def add(self, t: T, keys: List[str]):
        self.data.append((t, keys))
        num = self.data.__len__() - 1
        for key in keys:
            indexV = set()
            if key in self.index:
                indexV = self.index[key]
            indexV.add(num)
            self.index[key] = indexV

    def search(self, key: str) -> List[Tuple[int, T]]:
        if key in self.index:
            numSet: set[int] = self.index[key]
            return numSet.toList()\
                .map(lambda n: (n, self.data[n][0]))
        return list()

    def remove(self, num: int):
        if not num in self.data:
            return
        tup = self.data[num]
        t = tup[0]
        keys = tup[1]
        self.data[num] = None

        for key in keys:
            if not key in self.index:
                continue
            numSet = self.index[key]
            numSet.remove(num)
            if len(numSet) == 0:
                del self.index[key]
            else:
                self.index[key] = numSet

    def vs(self) -> List[T]:
        return self.data.map(lambda t: t[0])


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

        tmpKeys: List[str] = list()
        tmpKeys.append(key)

        while len(tmpKeys) > 0:
            ts = list()
            for tmp in tmpKeys:
                ts.appendAll(self.getChildrenKeys(tmp))

            tmpKeys.clear()
            tmpKeys.appendAll(ts)

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
            childKeys: set[int] = self.child[key]
            return childKeys.toList().map(lambda k: self.data[k][1])
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

    def values(self):
        return self.data.vs().map(lambda t: t[1])
