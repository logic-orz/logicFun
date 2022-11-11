
from unicodedata import name
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import JSON, Column, String, Text, create_engine, Integer, DateTime, and_, or_
from cttqFuncs.basic.exClass import Tree, IndexList
from ..data import *
from cttqFuncs.basic.exFunc import *
from cttqFuncs.basic.signClass import doBefore, doAfter

from sqlalchemy import event

Base = declarative_base()


class DbNode(Base):
    __tablename__ = 'nodes'
    key = Column(String(300), name='key', primary_key=True)
    infos = Column(Text, name='infos')
    tags = Column(Text, name='tags')


class DbEdge(Base):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fromKey = Column(String(300), name='from_key', index=True)
    toKey = Column(String(300), name='to_key', index=True)
    relaName = Column(String(50), name='rela_name')
    infos = Column(Text, name='infos')
    tags = Column(Text, name='tags')


def parseNode(self, node: Node):
    o = DbNode()
    o.key = node.key
    o.infos = node.infos.map(lambda i: i.toDict()).toStr()
    o.tags = node.tags.toStr()
    return {'node': o}


def parseEdge(self, edge: Edge):
    o = DbEdge()
    o.fromKey = edge.fromKey
    o.toKey = edge.toKey
    o.infos = edge.infos.map(lambda i: i.toDict()).toStr()
    o.tags = edge.tags.toStr()
    return {'edge': o}


def deParse(objs):
    def func(obj):
        if isinstance(obj, DbNode):
            o = Node()
            o.key = obj.key
        else:
            o = Edge()
            o.fromKey = obj.fromKey
            o.toKey = obj.toKey

        o.infos = obj.infos.toJson().map(lambda j: Info().build(j))
        o.tags = obj.tags.toJson()
        return o

    if isinstance(objs, List):
        return objs.map(lambda obj: func(obj))
    else:
        return func(objs)


class SqlDbGraph(Graph, GraphFunc):

    def __init__(self, name, engine) -> None:
        Graph.__init__(self, name)
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine,
                                 tables=[
                                     DbNode.__table__,
                                     DbEdge.__table__
                                 ], checkfirst=True)

    @doAfter(func=deParse)
    def queryNode(self, key: str, isFuzzy: bool = False) -> List[Node]:
        with self.Session() as session:
            res = session.query(DbNode)

            if isFuzzy:
                res = res.filter(DbNode.key.like('%'+key+'%'))
            else:
                res = res.filter(DbNode.key == key)

            return res.limit(10).all()

    @doAfter(func=deParse)
    def queryEdge(self, nodeKey: str, direct: int = 0) -> List[Edge]:
        with self.Session() as session:
            res = session.query(DbEdge)

            if direct == 1:
                return res.filter(DbEdge.fromKey == nodeKey).all()
            elif direct == -1:
                return res.filter(DbEdge.toKey == nodeKey).all()
            else:
                return res.filter(or_(DbEdge.fromKey == nodeKey, DbEdge.toKey == nodeKey)).all()

    @doBefore(func=parseNode)
    def addNode(self, node: Node):
        self.nodes[node.key] = node
        return self

    @doBefore(func=parseEdge)
    def addEdge(self, edge: Edge):
        self.edges.append(edge)
        return self

    def commit(self):
        i = 0
        with self.Session() as session:
            for node in self.nodes.vs():
                i += 1
                session.merge(node)
                if i % 500 == 0:
                    session.commit()
            session.commit()
            for edge in self.edges:
                i += 1
                session.add(edge)
                if i % 500 == 0:
                    session.commit()

            session.commit()

    @doAfter(func=deParse)
    def allEdges(self) -> List[Edge]:
        with self.Session() as session:
            return session.query(DbEdge).all()

    @doAfter(func=deParse)
    def allNodes(self) -> List[Node]:
        with self.Session() as session:
            return session.query(DbNode).all()
