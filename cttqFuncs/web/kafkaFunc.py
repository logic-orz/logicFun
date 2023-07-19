# -*- coding: utf-8 -*-

import json
import random
import time

import ujson
from kafka import KafkaConsumer, KafkaProducer
from loguru import logger as log


class KafkaOperate(object):
    groupId: str = 'my_group'
    

    def __init__(self, servers):
        if not servers:
            raise Exception('bootstrap_servers is None')
        self._servers = None
        if isinstance(servers, str):
            ip_port = servers.strip()
            if ',' in ip_port:
                self._servers = ip_port.replace(' ', '')\
                    .split(',')
            else:
                self._servers = [ip_port]

        self.producer = None
        self.consumer = None

        pass

    def __del__(self):
        pass

    def kfk_consume(self, topic=None):
        if not self.consumer:
            self.consumer = KafkaConsumer(
                topic=topic,
                group_id=self.groupId,
                bootstrap_servers=self._servers,
                auto_offset_reset='earliest',
            )
        count = 0
        for msg in self.consumer:
            count += 1
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            info = f'[{count}] {msg.topic}:{msg.partition}:{msg.offset}: key={msg.key}, value={msg.value.decode("utf-8")}'
            log.info(info)
            time.sleep(1)

    def _produce(self, topic=None, keyStr=None, data=None, partition=None):
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
       
        if partition:
            self.producer.send(
                topic=name,
                value=data,
                # key='count_num',  # 同一个key值，会被送至同一个分区
                partition=partition
            )
        else:
            self.producer.send(topic, data)
        pass

    def produce_one(self, topic=None, data=None, partition=None, partition_count=1):
        partition = partition if partition else random.randint(
            0, partition_count-1)
        self._produce(topic_name=topic,
                           data_dict=data,
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
        pass

    @staticmethod
    def get_consumer(group_id: str, servers: list, topic: str, enable_auto_commit=True) -> KafkaConsumer:
        topics = tuple([x.strip() for x in topic.split(',') if x.strip()])
        if enable_auto_commit:
            return KafkaConsumer(
                *topics,
                group_id=group_id,
                bootstrap_servers=servers,
                auto_offset_reset='earliest',
                # fetch_max_bytes=FETCH_MAX_BYTES,
                # connections_max_idle_ms=CONNECTIONS_MAX_IDLE_MS,
                # max_poll_interval_ms=KAFKA_MAX_POLL_INTERVAL_MS,
                # session_timeout_ms=SESSION_TIMEOUT_MS,
                # max_poll_records=KAFKA_MAX_POLL_RECORDS,
                # request_timeout_ms=REQUEST_TIMEOUT_MS,
                # auto_commit_interval_ms=AUTO_COMMIT_INTERVAL_MS,
                value_deserializer=lambda m: ujson.loads(m.decode('utf-8'))
            )
        else:
            return KafkaConsumer(
                *topics,
                group_id=group_id,
                bootstrap_servers=servers,
                auto_offset_reset='earliest',
                # fetch_max_bytes=FETCH_MAX_BYTES,
                # connections_max_idle_ms=CONNECTIONS_MAX_IDLE_MS,
                # max_poll_interval_ms=KAFKA_MAX_POLL_INTERVAL_MS,
                # session_timeout_ms=SESSION_TIMEOUT_MS,
                # max_poll_records=KAFKA_MAX_POLL_RECORDS,
                # request_timeout_ms=REQUEST_TIMEOUT_MS,
                enable_auto_commit=enable_auto_commit,
                value_deserializer=lambda m: ujson.loads(m.decode('utf-8'))
            )

    @staticmethod
    def get_producer(servers: list):
        return KafkaProducer(bootstrap_servers=servers, retries=5)
