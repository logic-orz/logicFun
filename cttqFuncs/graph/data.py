import cttqFuncs.basic.exFunc
from cttqFuncs.basic.exClass import StrBuild, BaseClass
from cttqFuncs.basic.signClass import build, toDict, toStr, doAfter, doBefore
from enum import Enum
from typing import Dict, Any, List
import abc
from abc import ABCMeta


class Tag:
    """
     * 数据标签封装类\n
     @ IsPrivate  属性是否为私有\n
     @ IsMore  属性是否为多值\n
     @ IsDirected  是否为有向关系（正向）\n
    """
    IsPrivate = 'isPrivate'
    IsMore = 'isMore'
    IsDirected = 'isDirected'

    def __init__(self) -> None:
        self.tags: Dict[str, Any] = {}

    def addTag(self, k, v):
        self.tags[k] = v
        return self

    def addTags(self, tag: Dict[str, Any]):
        self.tags.update(tag)
        return self

    def removeTag(self, k):
        del self.tags[k]
        return self


class Info(Tag, BaseClass):
    """
     * spo 属性定义类\n
     @ Name  实体名称\n
     @ NameKey  实体唯一消歧\n
     @ Concept  实体概念\n
     @ ConceptKey 实体概念消歧\n
     @ RelaName 关系名称\n
     @ Label 标签\n
    """
    Name = 'name'
    NameKey = 'nameKey'

    Concept = 'concept'
    ConceptKey = 'conceptKey'

    FromName = 'fromName'
    FromNameKey = 'fromNameKey'

    FromConcept = 'fromConcept'
    FromConceptKey = 'fromConceptKey'

    ToName = 'toName'
    ToNameKey = 'toNameKey'

    ToConcept = 'toConcept'
    ToConceptKey = 'toConceptKey'

    RelaName = 'relaName'

    Label = "label"

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

    def addInfo(self, name: str, value: Any):
        self.infos.append(Info(name, value))
        return self

    def getInfo(self, name: str) -> List[Info]:
        return self.infos.filter(lambda i: i.name == name)

    def getFirstInfoValue(self, name: str) -> Any:
        tmp: List[Info] = self.infos.filter(lambda i: i.name == name)
        if tmp.isEmpty():
            return None
        else:
            return tmp[0].value

    def removeInfo(self, name):
        self.infos = self.infos.filter(lambda info: info.name != name)
        return self


def infoToDict(d):
    d['info'] = d['info'].map(lambda i: i.toDict())
    return d


class Node(Tag, InfoBean, BaseClass):
    """
    * 图节点 定义类
    """

    def __init__(self, key: str = None):
        Tag.__init__(self)
        InfoBean.__init__(self)
        self.key: str = key

    @doAfter(func=infoToDict)
    def toDict(self):
        return BaseClass.toDict(self)


class Edge(Tag, InfoBean, BaseClass):
    """
    * 图关系 定义类
    """

    def __init__(self, fromKey=None, toKey=None) -> None:
        Tag.__init__(self)
        InfoBean.__init__(self)
        self.fromKey = fromKey
        self.toKey = toKey

    @doAfter(func=infoToDict)
    def toDict(self):
        return BaseClass.toDict(self)


class GraphFunc(metaclass=ABCMeta):
    """
    图对象 方法
    """

    @abc.abstractmethod
    def allEdges(self) -> List[Edge]:
        pass

    @abc.abstractmethod
    def allNodes(self) -> List[Node]:
        pass

    @abc.abstractmethod
    def addNode(self, node: Node):
        pass

    @abc.abstractmethod
    def addEdge(self, edge: Edge):
        pass

    @abc.abstractmethod
    # 节点检索
    def queryNode(self, key: str, isFuzzy: bool = False) -> List[Node]:
        #   todo 子类实现
        pass

    @abc.abstractmethod
    def queryEdge(self, nodeKey: str) -> List[Edge]:  # * 一度 关系检索
        #   todo 子类实现
        pass


@build
@toStr
class Graph(Tag):
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
