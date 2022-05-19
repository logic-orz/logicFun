'''
Author: Logic
Date: 2022-04-20 14:27:43
LastEditTime: 2022-05-19 14:47:59
FilePath: \pyFuncs\cttqFuncs\conn\redisFunc.py
Description: 
'''
import redis  # 导入redis 模块

from rediscluster import RedisCluster

from .dbFunc import DbConfig
from cttqFuncs.basic.configFunc import getDict


class Redis:
    def __init__(self, config: DbConfig):
        self.pool = redis.ConnectionPool(host=config.host,
                                         port=int(config.port),
                                         password=config.pwd,
                                         decode_responses=True,
                                         db=int(config.db) if config.db else 0)

    def cli(self):
        return redis.Redis(connection_pool=self.pool)

    def close(self):
        self.pool.disconnect()

    @staticmethod
    def fixedRedis(ns: str = 'redis'):
        return Redis(DbConfig().build(getDict(ns)))


class RedisClu:

    def __init__(self, config: DbConfig):
        redis_nodes = [
        ]
        hosts = config.hosts
        for s in hosts.split(","):
            arr = s.split(":", 1)
            redis_nodes.append(
                {
                    'host': arr[0], 'port': int(arr[1])
                }
            )

        self.conn = RedisCluster(
            startup_nodes=redis_nodes,
            password=config.pwd)

    def cli(self):
        return self.conn

    def close(self):
        self.conn.close()

    def fixedRedisClu(ns: str = 'redis'):
        return RedisClu(DbConfig().build(getDict(ns)))
