'''
Author: Logic
Date: 2022-04-20 14:27:43
LastEditTime: 2022-04-21 14:00:18
FilePath: \py_func_manage\myFunc\redisFunc.py
Description: 
'''
import redis  # 导入redis 模块

from rediscluster import RedisCluster


class Redis:
    # pool = None
    def __init__(self, config: dict):
        self.pool = redis.ConnectionPool(host=config['host'],
                                         port=int(config['port']),
                                         password=config['pwd'],
                                         decode_responses=True)

    def cli(self):
        return redis.Redis(connection_pool=self.pool)

    def close(self):
        self.pool.disconnect()


class RedisClu:

    def __init__(self, config: dict):
        redis_nodes = [
        ]
        hosts = config['hosts']
        for s in hosts.split(","):
            arr = s.split(":", 1)
            redis_nodes.append(
                {
                    'host': arr[0], 'port': int(arr[1])
                }
            )

        self.conn = RedisCluster(
            startup_nodes=redis_nodes,
            password=config['pwd'])

    def cli(self):
        return self.conn

    def close(self):
        self.conn.close()
