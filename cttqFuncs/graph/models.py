import abc
from abc import ABCMeta
from enum import Enum
from typing import Dict, List

from ..basic.exClass import BaseClass, CommonException
from ..basic.signClass import toStr
from ..exFunc import *


class Node(BaseClass):
    """
    * 图节点 定义类
    """

    @abc.abstractmethod
    def key(self) -> str:
        raise CommonException("方法未定义")


class Edge(BaseClass):
    """
    * 图关系 定义类
    """
    @abc.abstractmethod
    def fromKey(self) -> str:
        raise CommonException("方法未定义")

    @abc.abstractmethod
    def toKey(self) -> str:
        raise CommonException("方法未定义")


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
    def queryNode(self, key: str) -> List[Node]:
        #   todo 子类实现
        pass

    @abc.abstractmethod
    # * 一度 关系检索
    def queryEdge(self, nodeKey: str, direct: int = 0) -> List[Edge]:
        #   todo 子类实现
        pass


@toStr
class Graph(GraphFunc):
    """
    * 图结构 定义类
    """

    def __init__(self, name: str = None) -> None:
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
