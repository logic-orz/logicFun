
from sqlalchemy import ( Column,Integer, String, or_)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from basic.exFunc import *

from ..models import Edge, GraphFunc, Node

Base = declarative_base()


class DbNode(Base,Node):
    __tablename__ = 'nodes'
    name = Column(String(300), name='name', primary_key=True)
    age = Column(Integer)
    address=Column(String(500))
    
    def key(self):
        return self.name
    
class DbEdge(Base,Edge):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_name = Column(String(300),  index=True)
    to_name = Column(String(300),index=True)
    sss = Column(String(50), )
    def fromKey(self) -> str:
        return self.from_name
    
    def toKey(self) -> str:
        return self.to_name
    
    

class SqlDbGraph(GraphFunc):

    def __init__(self, name, engine) -> None:
        self.name=name
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine,
                                 tables=[
                                     DbNode.__table__,
                                     DbEdge.__table__
                                 ], checkfirst=True)

    def queryNode(self, key: str, isFuzzy: bool = False) -> List[DbNode]:
        with self.Session() as session:
            res = session.query(DbNode)

            if isFuzzy:
                res = res.filter(DbNode.name.like('%'+key+'%'))
            else:
                res = res.filter(DbNode.name == key)

            return res.limit(10).all()

    def queryEdge(self, nodeKey: str, direct: int = 0) -> List[DbEdge]:
        with self.Session() as session:
            res = session.query(DbEdge)

            if direct == 1:
                return res.filter(DbEdge.from_name == nodeKey).all()
            elif direct == -1:
                return res.filter(DbEdge.to_name == nodeKey).all()
            else:
                return res.filter(or_(DbEdge.from_name == nodeKey, DbEdge.to_name == nodeKey)).all()

    def addNode(self, node: DbNode):
        with self.Session() as session:
            session.add(node)
            session.commit()
            
    def addEdge(self, edge: DbEdge):
       with self.Session() as session:
            session.add(edge)
            session.commit()

    def allEdges(self) -> List[DbEdge]:
        with self.Session() as session:
            return session.query(DbEdge).all()

    def allNodes(self) -> List[DbNode]:
        with self.Session() as session:
            return session.query(DbNode).all()
