from typing import Dict, List

import motor.motor_asyncio
import pymongo
from pymongo.collection import Collection, ObjectId, ReturnDocument
from pymongo.database import Database
from pymongo.results import (BulkWriteResult, DeleteResult, InsertManyResult,
                             InsertOneResult, UpdateResult)

from ..basic import getDict
from .dbFunc import DbConfig, DbFunc


def parseObjIdWithDicts(docs: List[Dict]) -> List[Dict]:
    for doc in docs:
        if doc['_id'] and isinstance(doc['_id'], ObjectId):
            doc['id'] = str(doc['_id'])
            del doc['_id']
    return docs


def parseObjIds(objIds: List[ObjectId]) -> List[str]:
    res = []
    for objId in objIds:
        res.append(str(objId))
    return res


def toObjIdWithDicts(docs: List[Dict]) -> List[Dict]:
    for doc in docs:
        if doc['id'] and isinstance(doc['id'], str):
            doc['_id'] = ObjectId(doc['id'])
            del doc['id']
    return docs


def toObjIds(ids: List[str]) -> List[ObjectId]:
    res = []
    for id in ids:
        res.append(ObjectId(id))
    return res


class MongoDB():
    def __init__(self, config: DbConfig) -> None:
        self.client = pymongo.MongoClient(f"mongodb://{config.host}:{config.port}/")
        self.db: Database = self.client[config.db]  # 选择数据库

    def coll(self, tb: str) -> Collection:
        collection: Collection = self.db[tb]
        return collection

    def query(self, tb, filter: dict, pageNo: int = None, pageSize: int = None):
        coll = self.coll(tb)

        results = coll.find(filter)
        if pageNo and pageSize:
            results = results.skip((pageNo-1)*pageSize).limit(pageSize)

        re = []
        for doc in results:
            re.append(doc)

        return parseObjIdWithDicts(re)

    def delete(self, tb, filter: dict, optMany: bool = False):
        coll = self.coll(tb)
        if optMany:
            coll.delete_many(filter)
        else:
            coll.delete_one(filter)

    def insert(self, tb: str, datas: List[dict]):
        for data in datas:
            if '_id' in data:
                del data['_id']

            if 'id' in data:
                del data['id']

        coll = self.coll(tb)
        coll.insert_many(datas)

    def update(self, tb, data, filter: dict, optMany: bool = False):
        coll = self.coll(tb)

        if '_id' in data:
            del data['_id']

        if 'id' in data:
            del data['id']

        if optMany:
            coll.update_many(filter, data)
        else:
            coll.update_one(filter, data)

    def aggregate(self, tb: str, agg: List[dict]):
        self.coll(tb).aggregate(agg)

    def count(self, tb: str, query: dict):
        return self.coll(tb).count_documents(query)

    def tables(self):
        return self.db.list_collection_names()

    @classmethod
    def fix(cls, ns: str = 'mongodb'):
        return cls(DbConfig.build(getDict(ns)))


class MongoDBAsync():
    def __init__(self, config: DbConfig) -> None:

        self.client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{config.host}:{config.port}/")
        self.db = self.client[config.db]

    def coll(self, tb: str) -> Collection:

        collection: Collection = self.db[tb]
        return collection

    async def query(self, tb, filter: dict, pageNo: int = None, pageSize: int = None):
        coll = self.coll(tb)

        results = coll.find(filter)
        if pageNo and pageSize:
            results = results.skip((pageNo-1)*pageSize).limit(pageSize)

        res = []
        async for doc in results:
            res.append(doc)

        return parseObjIdWithDicts(res)

    async def delete(self, tb, filter: dict, optMany: bool = False):
        coll = self.coll(tb)
        if optMany:
            await coll.delete_many(filter)
        else:
            await coll.delete_one(filter)

    async def insert(self, tb: str, datas: List[dict]):
        for data in datas:
            if '_id' in data:
                del data['_id']

            if 'id' in data:
                del data['id']

        coll = self.coll(tb)
        await coll.insert_many(datas)

    async def update(self, tb, data, filter: dict, optMany: bool = False):
        coll = self.coll(tb)
        if '_id' in data:
            del data['_id']

        if 'id' in data:
            del data['id']

        if optMany:
            await coll.update_many(filter, data)
        else:
            await coll.update_one(filter, data)

    async def aggregate(self, tb: str, agg: List[dict]):
        return await self.coll(tb).aggregate(agg)

    async def count(self, tb: str, filter: dict):
        return await self.coll(tb).count_documents(filter)

    async def tables(self):
        return await self.db.list_collection_names()

    @classmethod
    def fix(cls, ns: str = 'mongodb'):
        return cls(DbConfig.build(getDict(ns)))
