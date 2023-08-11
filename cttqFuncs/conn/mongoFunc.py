import pymongo
from .dbFunc import DbConfig
from pymongo.collection import Collection
from pymongo.results import InsertManyResult, InsertOneResult, BulkWriteResult, UpdateResult, DeleteResult


class Mongo():
    def __init__(self, config: DbConfig) -> None:
        self.client = pymongo.MongoClient(f"mongodb://{config.address}:{config.port}/")
        self.db = config.db  # 选择数据库
        pass

    def collection(self, tb: str, db=None) -> Collection:
        if not db:
            db = self.db
        collection: Collection = self.client[db][tb]
        return collection

    # def query(self, tb, data: dict, db: str = None):
    #     coll = self.collection(tb, db)
    #     results = coll.find(data)
    #     re = []
    #     for doc in results:
    #         re.append(doc)
    #     return re
