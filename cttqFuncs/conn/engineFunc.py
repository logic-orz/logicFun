from .dbFunc import DbConfig
from cttqFuncs.basic.configFunc import getDict
from urllib.parse import quote_plus as urlquote


def mySqlEngine(ns: str = 'mysql',isAsync=False):

    config = DbConfig.build(getDict(ns))
    if isAsync:
        from sqlalchemy.ext.asyncio import create_async_engine as create_engine
        driver='aiomysql'
    else:
        from sqlalchemy import create_engine
        driver='pymysql'
    
    DB_CONNECT = f'mysql+{driver}://{config.user}:{urlquote(config.pwd)}@{config.host}:{config.port}/{config.db}?charset=utf8'

    engine = create_engine(
        DB_CONNECT, future=True,
        max_overflow=5,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        pool_pre_ping=True,
    )
    return engine

def postGresEngine(ns: str = 'postgres',isAsync=False):

    config = DbConfig().build(getDict(ns))
    
    DB_CONNECT = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
        config.user, urlquote(config.pwd), config.host, config.port, config.db)

    from sqlalchemy import create_engine
    engine = create_engine(
        DB_CONNECT,
        max_overflow=5,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=3600,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        pool_pre_ping=True,
    )
    return engine
