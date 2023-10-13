from typing import List
import pymongo
from .dbFunc import DbConfig, DbFunc
from pymongo.collection import Collection, ReturnDocument, ObjectId
from pymongo.database import Database
from pymongo.results import InsertManyResult, InsertOneResult, BulkWriteResult, UpdateResult, DeleteResult
from ..basic import getDict


class MongoDB():
    def __init__(self, config: DbConfig) -> None:
        self.client = pymongo.MongoClient(f"mongodb://{config.host}:{config.port}/")
        self.db: Database = self.client[config.db]  # 选择数据库
        pass

    def coll(self, tb: str) -> Collection:

        collection: Collection = self.db[tb]
        return collection

    def query(self, tb, data: dict, pageNo: int = None, pageSize: int = None):
        coll = self.coll(tb)

        results = coll.find(data)
        if pageNo and pageSize:
            results = results.skip((pageNo-1)*pageSize).limit(pageSize)

        re = []
        for doc in results:
            if doc['_id']:
                tId: ObjectId = doc['_id']
                doc['_id'] = str(tId)

            re.append(doc)
        return re

    def delete(self, tb, data: dict, optMany: bool = False):
        coll = self.coll(tb)
        if data['_id']:
            tId: str = data['_id']
            data['_id'] = ObjectId(tId)

        if optMany:
            coll.delete_many(data)
        else:
            coll.delete_one(data)

    def insert(self, tb: str, datas: List[dict]):
        for data in datas:
            if '_id' in data:
                del data['_id']
        coll = self.coll(tb)
        coll.insert_many(datas)

    def update(self, tb, data, filter=None, optMany: bool = False):
        coll = self.coll(tb)
        if data['_id']:
            tId: str = data['_id']
            data['_id'] = ObjectId(tId)

        if optMany:
            coll.update_many(filter, data)
        else:
            coll.update_one(filter, data)

    def aggregate(self, tb: str, agg: List[dict]):
        self.coll(tb).aggregate(agg)

    def count(self, tb: str, query):
        return self.coll(tb).count_documents(query)

    def tables(self):
        return self.db.list_collection_names()

    @classmethod
    def fix(cls, ns: str = None):
        if not ns:
            ns = cls.__name__.lower()
        return cls(DbConfig.build(getDict(ns)))
