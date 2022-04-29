'''
Author: Logic
Date: 2022-04-27 09:41:14
LastEditTime: 2022-04-28 19:03:02
FilePath: \pyFuncs\graph\beans.py
Description: 
'''

from myFunc.basic.myClass import IndexList, BaseClass
import myFunc.basic.signFunc
from enum import Enum
from typing import Dict, Any, List, overload


class TagKey(Enum):
    isPrivate = 'isPrivate',
    isMore = 'isMore'


class InfoName(Enum):
    name = 'name',
    nameTag = 'nameTag',
    concept = 'concept',
    conceptTag = 'conceptTag'


class TagBean:  # * 数据标签封装类
    def __init__(self) -> None:
        self.tags: Dict[str, Any] = {}

    def addTag(self, k, v):
        self.tags[k] = v
        return self

    def removeTag(self, k):
        del self.tags[k]
        return self


class Info(TagBean,BaseClass):  # * spo 属性定义类
    def __init__(self) -> None:
        super().__init__()
        self.name: str = None
        self.value: Any = None

    @overload
    def build(self, name: str, value: Any):
        self.name = name
        self.value = value
        return self


class InfoBean:  # * 属性集合封装类
    def __init__(self) -> None:
        self.infos: List[Info] = []

    def addInfo(self, info: Info):
        self.infos.append(info)
        return self

    def addInfo(self, infos: List[Info]):
        for info in infos:
            self.infos.append(info)
        return self

    def addInfo(self, name: str, value: Any):
        self.infos.append(Info().build(name, value))
        return self

    def removeInfo(self, name):
        self.infos = self.infos.filter(lambda info: info.name != name)
        return self


class Node(TagBean, InfoBean,BaseClass):  # * 图节点 定义类
    def __init__(self) -> None:
        super().__init__()
        self.key: str = None

    @overload
    def build(self, key, tags=None, infos=None):
        self.key = key
        if tags:
            self.tags = tags
        if infos:
            self.infos = infos
        return self


class Edge(TagBean, InfoBean,BaseClass):  # * 图关系 定义类

    def __init__(self) -> None:
        super().__init__()
        self.fromKey: str = None
        self.toKey: str = None

    @overload
    def build(self, fromKey, toKey, tags=None, infos=None):
        self.fromKey = fromKey
        self.toKey = toKey
        if tags:
            self.tags = tags
        if infos:
            self.infos = infos
        return self


class Graph(TagBean,BaseClass):  # * 图结构 定义类

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.nodes: List[Node] = list()
        self.edges: List[Edge] = list()

    def toDict(self):
        return {'name': self.name,
                'tags': self.tags,
                'nodes': self.nodes.map(lambda n: n.toDict()),
                'edges': self.edges.map(lambda n: n.toDict())
                }


class IndexGraph(TagBean,BaseClass):  # * 图结构 定义类
    def __init__(self, name) -> None:
        super().__init__()
        self.name: str = name
        self.nodes: Dict[str, Node] = dict()
        self.edges: IndexList[Edge] = IndexList()

    def toDict(self):
        return {
            'name': self.name,
            'tags': self.tags,
            'nodes': self.nodes.vs().map(lambda n: n.toDict()),
            'edges': self.edges.vs().map(lambda n: n.toDict())
        }
