
import myFunc.basic.signFunc
from myFunc.basic.myClass import IndexList, Tree
from myFunc.basic.fileFunc import readLines
from myFunc.graph.data import *
from myFunc.graph.schema import Concept, Relation


class IndexGraph(Graph, GraphFunc):
    """
    * 图结构 定义类 用于内存索引
    """

    def __init__(self, name) -> None:
        super().__init__(name)
        self.nodes: IndexList[Node] = IndexList()
        self.edges: IndexList[Edge] = IndexList()

    def toDict(self):
        return {
            'name': self.name,
            'tags': self.tags,
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
