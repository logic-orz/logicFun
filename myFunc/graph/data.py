from myFunc.basic.myClass import BaseClass
from myFunc.basic.signFunc import *
from enum import Enum
from typing import Dict, Any, List
import abc
from abc import ABCMeta


class Tag:
    """
     * 数据标签封装类
    """
    IsPrivate = 'isPrivate'  # ? 属性是否为私有
    IsMore = 'isMore'  # ? 属性是否为多值
    IsDirected = 'isDirected'  # ? 是否为有向关系（正向）

    def __init__(self) -> None:
        self.tags: Dict[str, Any] = {}

    def addTag(self, k, v):
        self.tags[k] = v
        return self

    def removeTag(self, k):
        del self.tags[k]
        return self


class Info(Tag, BaseClass):
    """
    * spo 属性定义类
    """
    Name = 'name'  # ? 实体名称
    NameTag = 'nameTag'  # ? 实体名称消歧

    Concept = 'concept'  # ? 实体概念
    ConceptTag = 'conceptTag'  # ? 实体概念消歧

    FromName = 'fromName'
    FromNameTag = 'fromNameTag'

    FromConcept = 'fromConcept'
    FromConceptTag = 'fromConceptTag'

    ToName = 'toName'
    ToNameTag = 'toNameTag'

    ToConcept = 'toConcept'
    ToConceptTag = 'toConceptTag'

    RelaName = 'relaName'  # ? 关系名称

    Label = "label"  # ? 标签

    def __init__(self, name: str = None, value: Any = None):
        Tag.__init__(self)
        self.name = name
        self.value = value


class InfoBean:
    """
    * 属性集合封装类
    """

    def __init__(self) -> None:
        self.infos: List[Info] = []

    def addInfos(self, infos: List[Info]):
        for info in infos:
            self.infos.append(info)
        return self

    def getInfo(self, name: str) -> List[Info]:
        return self.infos.filter(lambda i: i.name == name)

    def getFirstInfoValue(self, name: str) -> Any:
        tmp: List[Info] = self.infos.filter(lambda i: i.name == name)
        if tmp.isEmpty():
            return None
        else:
            return tmp[0].value

    def addInfo(self, name: str, value: Any):
        self.infos.append(Info(name, value))
        return self

    def removeInfo(self, name):
        self.infos = self.infos.filter(lambda info: info.name != name)
        return self


class Node(Tag, InfoBean, BaseClass):
    """
    * 图节点 定义类
    """

    def __init__(self, key: str = None, tags: dict = None, infos: List[Info] = None):
        Tag.__init__(self)
        InfoBean.__init__(self)
        self.key: str = key
        if tags:
            self.tags = tags
        if infos:
            self.infos = infos

    def toDict(self):
        return {"key": self.key, "tags": self.tags, "infos": self.infos.map(lambda i: i.toDict())}


class Edge(Tag, InfoBean, BaseClass):
    """
    * 图关系 定义类
    """

    def __init__(self, fromKey=None, toKey=None, tags: dict = None, infos: List[Info] = None) -> None:
        Tag.__init__(self)
        InfoBean.__init__(self)
        self.fromKey = fromKey
        self.toKey = toKey
        if tags:
            self.tags = tags
        if infos:
            self.infos = infos

    def toDict(self):
        return {"fromKey": self.fromKey, "toKey": self.toKey, "tags": self.tags, "infos": self.infos.map(lambda i: i.toDict())}


class GraphFunc(metaclass=ABCMeta):
    """
    图对象 方法
    """

    @abc.abstractmethod
    def addNode(self, node: Node):
        pass

    @abc.abstractmethod
    def addEdge(self, edge: Edge):
        pass

    @abc.abstractmethod
    def queryNode(self, key: str, isFuzzy: bool = False) -> List[Node]:  # 节点检索
        #   todo 子类实现
        pass

    @abc.abstractmethod
    def queryEdge(self, nodeKey: str) -> List[Edge]:  # * 一度 关系检索
        #   todo 子类实现
        pass


class Graph(Tag, BaseClass):
    """
    * 图结构 定义类
    """

    def __init__(self, name: str = None) -> None:
        Tag.__init__(self)
        self.name: str = name
        self.nodes: Dict[str, Node] = dict()
        self.edges: List[Edge] = list()

    def toDict(self):
        return {'name': self.name,
                'tags': self.tags,
                'nodes': self.nodes.vs().map(lambda n: n.toDict()),
                'edges': self.edges.map(lambda n: n.toDict())
                }
