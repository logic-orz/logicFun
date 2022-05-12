
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import JSON, Column, String, Text, create_engine, Integer, DateTime, and_, or_
from myFunc.basic.myClass import Tree, IndexList
from myFunc.graph.data import *
from myFunc.basic.signFunc import *
from myFunc.graph.schema import Concept


Base = declarative_base()


class DbConcept(Base):
    __tablename__ = 't_concepts'
    key = Column(String(300), name='c_key', primary_key=True)
    parentKey = Column(String(300), name='c_parent_key')
    name = Column(String(300), name='c_name')
    nameTag = Column(String(300), name='c_name_tag')
    labels = Column(JSON, name='c_labels')
    attrs = Column(JSON, name='c_attrs')


class DbRelation(Base):
    __tablename__ = 't_relations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(300), name='c_key')
    fromKey: List[str] = Column(JSON, name='c_from_key')
    toKey: List[str] = Column(JSON, name='c_to_key')
    name = Column(String(300), name='c_name')
    desc = Column(String(300), name='c_desc')
    labels: List[str] = Column(JSON, name='c_labels')


class SqlDbSchema:

    def __init__(self) -> None:
        pass

    def save(concept: Concept, parentKey: str) -> None:
        pass

    def getByKey(key: str) -> Concept:
        pass

    def getByName(name: str) -> List[Concept]:
        pass

    """
    * 图结构 定义类 用于sqlite索引
    """


class DbNode(Base):
    __tablename__ = 'nodes'
    key: str = Column(String(300), name='c_key', primary_key=True)
    infos: List[Info] = Column(JSON, name='c_infos')
    tags: List[str] = Column(JSON, name='c_tags')

    def parse(self, node: Node):
        self.infos = node.infos.map(lambda i: json.loads(i.toStr()))
        self.key = node.key
        self.tags = node.tags
        return self

    def deParse(self):
        node = Node()
        node.key = self.key
        node.infos = self.infos.map(lambda j: Info().build(j))
        node.tags = self.tags
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


class SqlDbGraph(Graph, GraphFunc):

    def __init__(self, name, engine) -> None:
        Graph.__init__(self, name)
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine, tables=[
                                 DbNode.__tablename__, DbEdge.__tablename__, DbRelation.__tablename__, DbConcept.__tablename__], checkfirst=True)

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
