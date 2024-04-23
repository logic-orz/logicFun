from typing import Dict, List
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from .dbFunc import DbConfig

#
# pip install elasticsearch==5.5.3
#


class EsClient():
    def __init__(self, config: DbConfig) -> None:
        self.client = Elasticsearch(
            hosts=[{"host": config.host, "port": config.port}],
            sniff_on_start=True,    # 连接前测试
            sniff_on_connection_fail=True,  # 节点无响应时刷新节点
            sniff_timeout=60    # 设置超时时间
        )
        self.index = config.db

    def createIndex(self, indexName,):
        self.client.indices.create(index=indexName, ignore=400)

    def deleteIndex(self, indexName):
        self.client.indices.delete(index=indexName, ignore=400)

    def deleteByQuery(self, indexName):
        self.client.delete_by_query(index=indexName,
                                    body={
                                        "query": {
                                            "match_all": {}
                                        }
                                    },
                                    wait_for_completion=False
                                    )

    def insertOne(self, doc: dict):
        self.client.index(index=self.index, doc_type='_doc', body=doc)

    def insertMany(self, docs: List[Dict]):
        bulks = []
        for doc in docs:
            bulks.append({
                '_index': self.index,
                '_type': '_doc',
                '_source': doc
            })
        helpers.bulk(self.client, bulks)

    def query(self, query: dict):
        pass
