
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import JSON, Column, String, Text, create_engine, Integer, DateTime, and_, or_
from myFunc.graph.beans import *
from myFunc.basic.signFunc import *


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


Base = declarative_base()


class SqlDbGraph(Graph, GraphFunc):
    """
    * 图结构 定义类 用于sqlite索引
    """
    class DbNode(Base):
        __tablename__ = 'nodes'
        key = Column(String(300), name='c_key', primary_key=True)
        infos = Column(Text, name='c_infos')
        tags = Column(Text, name='c_tags')

        def parse(self, node: Node):
            self.infos = json.dumps(node.infos.map(
                lambda i: i.toDict()), ensure_ascii=False)
            self.key = node.key
            self.tags = json.dumps(node.tags, ensure_ascii=False)
            return self

        def deParse(self):
            node = Node()
            node.key = self.key
            node.infos = json.loads(self.infos).map(lambda j: Info().build(j))
            node.tags = json.loads(self.tags)
            return node

    class DbEdge(Base):
        __tablename__ = 'edges'
        id = Column(Integer, primary_key=True, autoincrement=True)
        fromKey = Column(String(300), name='c_from_key')
        toKey = Column(String(300), name='c_to_key')
        infos = Column(JSON, name='c_infos')
        tags = Column(JSON, name='c_tags')

        def parse(self, edge: Edge):
            self.infos = json.dumps(edge.infos.map(
                lambda i: i.toDict()), ensure_ascii=False)
            self.fromKey = edge.fromKey
            self.toKey = edge.toKey
            self.tags = json.dumps(edge.tags, ensure_ascii=False)
            return self

        def deParse(self):
            edge = Edge()
            edge.fromKey = self.fromKey
            edge.toKey = self.toKey
            edge.infos = json.loads(self.infos).map(lambda j: Info().build(j))
            edge.tags = json.loads(self.tags)
            return edge

    def __init__(self, name, engine) -> None:
        Graph.__init__(self, name)
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine, checkfirst=True)

    def queryNode(self, key: str, isFuzzy: bool = False) -> List[Node]:
        if isFuzzy:
            with self.Session() as session:
                return session.query(self.DbNode)\
                    .filter(self.DbNode.key.like('%'+key+'%'))\
                    .limit(10)\
                    .all()\
                    .map(lambda d: d.deParse())
        else:
            with self.Session() as session:
                return session.query(self.DbNode)\
                    .filter(self.DbNode.key == key)\
                    .limit(10)\
                    .all()\
                    .map(lambda d: d.deParse())

    def queryEdge(self, nodeKey: str) -> List[Edge]:
        with self.Session() as session:
            return session.query(self.DbEdge)\
                .filter(or_(self.DbEdge.fromKey == nodeKey, self.DbEdge.toKey == nodeKey))\
                .all()\
                .map(lambda d: d.deParse())

    def addNode(self, node: Node):
        self.nodes[node.key] = node

    def addEdge(self, edge: Edge):
        self.edges.append(edge)

    def commit(self):
        i = 0
        with self.Session() as session:
            for node in self.nodes.vs():
                i += 1
                session.merge(self.DbNode().parse(node))
                if i % 500 == 0:
                    session.commit()
            session.commit()
            for edge in self.edges:
                i += 1
                session.add(self.DbEdge().parse(edge))
                if i % 500 == 0:
                    session.commit()

            session.commit()
