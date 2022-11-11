import cttqFuncs.basic.exFunc
from cttqFuncs.basic.exClass import StrBuild, BaseClass
from cttqFuncs.basic.signClass import build, toDict, toStr, doAfter, doBefore
from enum import Enum
from typing import Dict, Any, List
import abc
from abc import ABCMeta
from enum import Enum


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

    # [(k,v)...]
    def addTag(self, *kvs):
        for k, v in kvs:
            self.tags[k] = v
        return self

    def addTags(self, tag: Dict[str, Any]):
        self.tags.update(tag)
        return self

    def removeTag(self, *ks):
        for k in ks:
            del self.tags[k]
        return self


class Info(Tag, BaseClass):
    """
     * spo 属性定义类\n
    """
    Name = 'name'

    FromName = 'fromName'

    ToName = 'toName'

    Label = "label"

    def __init__(self, name: str = None, value: Any = None):
        Tag.__init__(self)
        self.name = name
        self.value = value


class Infos:
    """
    * 属性集合封装类
    """

    def __init__(self) -> None:
        self.infos: List[Info] = []

    def addInfo(self, *infos: Info):
        for info in infos:
            self.infos.append(info)
        return self

    def getInfo(self, name: str) -> List[Info]:
        return self.infos.filter(lambda i: i.name == name)

    def getInfoValue(self, name: str) -> Any:
        tmp: List[Info] = self.infos.filter(
            lambda i: i.name == name).map(lambda i: i.value)

    def removeInfo(self, name):
        self.infos = self.infos.filter(lambda info: info.name != name)
        return self


def infoToDict(d):
    d['infos'] = d['infos'].map(lambda i: i.toDict())
    return d


class Node(Tag, Infos, BaseClass):
    """
    * 图节点 定义类
    """

    def __init__(self, name: str, key: str = None):
        Tag.__init__(self)
        Infos.__init__(self)
        self.name: str = name
        self.key: str = key if key else name

    @doAfter(func=infoToDict)
    def toDict(self):
        return BaseClass.toDict(self)


class Edge(Tag, Infos, BaseClass):
    """
    * 图关系 定义类
    """

    def __init__(self, fromKey=None, toKey=None, relaName: str = None) -> None:
        Tag.__init__(self)
        Infos.__init__(self)
        self.fromKey = fromKey
        self.toKey = toKey
        self.relaName = relaName

    @doAfter(func=infoToDict)
    def toDict(self):
        return BaseClass.toDict(self)


class Opt(Enum):

    Overwrite = 'overwrite'
    Update = 'update'
    Skip = 'skip'


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
    # * 一度 关系检索
    def queryEdge(self, nodeKey: str, direct: int = 0) -> List[Edge]:
        #   todo 子类实现
        pass


@build
@toStr
class Graph(Tag, GraphFunc):
    """
    * 图结构 定义类
    """

    def __init__(self, name: str = None) -> None:
        Tag.__init__(self)
        self.name: str = name
        self.nodes: Dict[str, Node] = dict()
        self.edges: List[Edge] = list()

    def allEdges(self) -> List[Edge]:
        return self.edges

    def allNodes(self) -> List[Node]:
        return self.nodes.vs()

    def addNode(self, node: Node, opt: Opt = Opt.Overwrite):
        if opt == Opt.Overwrite:
            self.nodes[node.key] = node
        elif opt == Opt.Skip:
            if node.key not in self.nodes:
                self.nodes[node.key] = node
        elif opt == Opt.Update:
            if node.key in self.nodes:
                tmp = self.nodes[node.key]

    def addEdge(self, edge: Edge):
        pass

    # 节点检索
    def queryNode(self, key: str, isFuzzy: bool = False) -> List[Node]:
        #   todo 子类实现
        pass

    # * 一度 关系检索
    def queryEdge(self, nodeKey: str, direct: int = 0) -> List[Edge]:
        #   todo 子类实现
        pass

    def toDict(self):
        return {'name': self.name,
                'tags': self.tags,
                'nodes': self.nodes.vs().map(lambda n: n.toDict()),
                'edges': self.edges.map(lambda n: n.toDict())
                }
