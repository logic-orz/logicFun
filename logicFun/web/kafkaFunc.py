# -*- coding: utf-8 -*-

import json
import random
import time
from typing import Callable

from kafka import KafkaConsumer, KafkaProducer
from loguru import logger as log
from pydantic import BaseModel


class KafkaOperate(object):
    groupId: str = 'my_group'

    def __init__(self, servers: str):
        if not servers:
            raise Exception('bootstrap_servers is None')

        self._servers = servers.strip()\
            .replace(' ', '')\
            .split(',')

        self.producer = None
        self.consumer = None

    def _consume(self, topic: str, batchSize: int = 100):
        if not self.consumer:
            self.consumer = KafkaConsumer(
                topic=topic,
                group_id=self.groupId,
                bootstrap_servers=self._servers
            )
        # for msg in self.consumer:
        #     doFunc(msg)
        msgs = self.consumer.poll(max_records=batchSize)
        return msgs

    def _produce(self, topic: str, data, keyStr: str = None, partition: int = None):
        """
            如果想要多线程进行消费，可以设置 发往不通的 partition
            有多少个 partition 就可以启多少个线程同时进行消费，
        :param topic_name:
        :param data_dict:
        :param partition:
        :return:
        """
        if not self.producer:
            self.producer = KafkaProducer(
                bootstrap_servers=self._servers,
                client_id=self.groupId,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

        self.producer.send(
            topic=topic,
            value=data,
            key=keyStr,  # 同一个key值，会被送至同一个分区
            partition=partition
        )

    def produce_one(self, topic: str, data, keyStr: str = None, partition=None):

        self._produce(topic=topic,
                      data=data,
                      keyStr=keyStr,
                      partition=partition)
        self.producer.flush()

    def produce_many(self, topic=None, data_list=None, partition=None, partition_count=1, per_count=100):
        count = 0
        for data in data_list:
            partition = partition if partition else count % partition_count
            self._produce(topic_name=topic,
                          data_dict=data,
                          partition=partition)
            if 0 == count % per_count:
                self.producer.flush()
            count += 1
        self.producer.flush()
