
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import JSON, Column, String, Text, create_engine, Integer, DateTime, and_, or_
from cttqFuncs.basic.exClass import ListEx, Tree, IndexList
from cttqFuncs.graph.data import *
from cttqFuncs.basic.exFunc import *
from cttqFuncs.basic.signClass import doBefore, doAfter

from cttqFuncs.graph.schema import Concept
from sqlalchemy import event

Base = declarative_base()


class DbConcept(Base):
    __tablename__ = 't_concepts'
    key = Column(String(300), name='c_key', primary_key=True)
    parentKey = Column(String(300), name='c_parent_key')
    name = Column(String(300), name='c_name')
    nameTag = Column(String(300), name='c_name_tag')
    labels = Column(Text, name='c_labels')
    attrs = Column(Text, name='c_attrs')


class DbRelation(Base):
    __tablename__ = 't_relations'
    id = Column(Integer, name='id', primary_key=True, autoincrement=True)
    key = Column(String(300), name='c_key')
    fromKey: ListEx[str] = Column(Text, name='c_from_key')
    toKey: ListEx[str] = Column(Text, name='c_to_key')
    name = Column(String(300), name='c_name')
    desc = Column(String(300), name='c_desc')
    labels: ListEx[str] = Column(JSON, name='c_labels')


class SqlDbSchema:

    def __init__(self) -> None:
        pass

    def save(concept: Concept, parentKey: str) -> None:
        pass

    def getByKey(key: str) -> Concept:
        pass

    def getByName(name: str) -> ListEx[Concept]:
        pass

    """
    * 图结构 定义类 用于sqlite索引
    """


class DbNode(Base):
    __tablename__ = 't_nodes'
    key = Column(String(300), name='c_key', primary_key=True)
    infos = Column(Text, name='c_infos')
    tags = Column(Text, name='c_tags')


class DbEdge(Base):
    __tablename__ = 't_edges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fromKey = Column(String(300), name='c_from_key')
    toKey = Column(String(300), name='c_to_key')
    infos = Column(Text, name='c_infos')
    tags = Column(Text, name='c_tags')


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
                                     DbEdge.__table__,
                                     DbRelation.__table__,
                                     DbConcept.__table__
                                 ], checkfirst=True)

    @doAfter(func=deParse)
    def queryNode(self, key: str, isFuzzy: bool = False) -> ListEx[Node]:
        with self.Session() as session:
            res = session.query(DbNode)

            if isFuzzy:
                res = res.filter(DbNode.key.like('%'+key+'%'))
            else:
                res = res.filter(DbNode.key == key)

            return res.limit(10).all()

    @doAfter(func=deParse)
    def queryEdge(self, nodeKey: str) -> List[Edge]:
        with self.Session() as session:
            return session.query(DbEdge)\
                .filter(or_(DbEdge.fromKey == nodeKey, DbEdge.toKey == nodeKey))\
                .all()

    @doBefore(func=parseNode)
    def addNode(self, node: Node):
        self.nodes[node.key] = node

    @doBefore(func=parseEdge)
    def addEdge(self, edge: Edge):
        self.edges.append(edge)

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
