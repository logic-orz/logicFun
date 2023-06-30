from urllib.parse import quote_plus as urlquote

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..basic import getDict
from ..exFunc import *
from .dbFunc import DbConfig

BaseModel=declarative_base()

def mySqlEngine(ns: str = 'mysql',isAsync=False):

    config = DbConfig.build(getDict(ns))
    if isAsync:
        from sqlalchemy.ext.asyncio import create_async_engine as create_engine
        driver='aiomysql'
    else:
        from sqlalchemy import create_engine
        driver='pymysql'
    
    db_connect_url = f'mysql+{driver}://{config.user}:{urlquote(config.pwd)}@{config.host}:{config.port}/{config.db}?charset=utf8'

    engine = create_engine(
        db_connect_url, 
        echo=False,
        future=True,
        max_overflow=5,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        pool_pre_ping=True,
    )
    if isAsync:
        Session=sessionmaker(bind=engine,class_=AsyncSession)
    else:
        Session=sessionmaker(bind=engine)
    return (engine,Session)


class OrmBuilder():

    @property
    def columns(self):
        return self.__class__.metadata.tables[self.__class__.__tablename__].columns._all_columns

    def buildByComment(self, data: Dict):
        cn = self.columns.map(lambda c: (c.comment, c.name)).toDict()
        for c, v in data.kvs():
            if c in cn:
                n = cn[c]
                self.__dict__[n] = v
        return self

    def toDictWithComment(self):
        data = self.__dict__
        cn = self.columns.map(lambda c: (c.name, c.comment)).toDict()
        for c, v in data.kvs():
            if c in cn:
                n = cn[c]
                data[n] = v
        return data
