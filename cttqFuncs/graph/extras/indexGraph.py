from typing import Dict, List, Set, Tuple

from ...basic.exClass import IndexList, Tree
from ...exFunc import *
from ..models import *


class IndexGraph(Graph, GraphFunc):
    """
    * 图结构 定义类 用于内存索引
    """
    nodes: IndexList[Node] = IndexList()
    edges: IndexList[Edge] = IndexList()

    def __init__(self, name) -> None:
        super().__init__(name)

    def toDict(self):
        return {
            'name': self.name,
            'nodes': self.nodes.vs().map(lambda n: n.toDict()),
            'edges': self.edges.vs().map(lambda n: n.toDict())
        }

    def queryNode(self, key: str) -> List[Node]:
        return self.nodes.search(key).map(lambda t: t[1])

    def queryEdge(self, nodeKey: str) -> List[Edge]:
        return self.edges.search(nodeKey).map(lambda t: t[1])

    def addNode(self, node: Node):
        self.nodes.add(node, [node.key])

    def addEdge(self, edge: Edge):
        self.edges.add(edge, [edge.fromKey, edge.toKey])
