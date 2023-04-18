from typing import Dict
from models import GraphFunc
from ...exFunc import *


class PageRank:

    times: int = 10
    d: float = 0.25

    def __init__(self, graph: GraphFunc) -> None:
        self.graph = graph

    def calculate(self):
        """
        * Dict[key,R值]
        """
        weight = self.graph.allNodes()\
            .map(lambda n: (n.key, float(1)))

        """
        * Dict[key,出度]
        """
        out: Dict[str, int] = self.graph.allEdges()\
            .map(lambda e: (e.fromKey, 1))\
            .reduceByKey(lambda a, b: a+b)

        """
        ? 1:List[Tuple[toKey,fromKey]] 
        ? 2:去重
        ? 3:List[Tuple[Tuple[toKey,to R值],单个from节点贡献的R值]
        ? 4:分组聚合,List[Tuple[Tuple[toKey,to R值],所有from节点贡献的R值之和]
        ? 5
        """

        weight = self.graph.allEdges()\
            .map(lambda e: (e.toKey, e.fromKey))\
            .distinct()\
            .map(lambda t: ((t[0], weight[t[0]]),  float(weight[t[1]])/float(out[t[1]])))\
            .reduceByKey(lambda a, b: a+b)\
            .map(lambda t: (t[0][0], t[0][1]*self.d + t[1]*(1 - self.d)))
        pass


class ShortestPath:

    def __init__(self, graph: GraphFunc) -> None:
        self.graph = graph
