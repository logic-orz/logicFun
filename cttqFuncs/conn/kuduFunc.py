from typing import Dict, List
import kudu
from datetime import datetime


class Kudu():

    def __init__(self, host: str, port: int) -> None:
        self.client = kudu.connect(host=host, port=port)

        # # 为新表定义架构
        # builder = kudu.schema_builder()
        # builder.add_column('key').type(
        #     kudu.int64).nullable(False).primary_key()
        # builder.add_column('ts_val', type_=kudu.unixtime_micros,
        #                    nullable=False, compression='lz4')
        # schema = builder.build()

        # # 定义分区模式
        # partitioning = Partitioning().add_hash_partitions(
        #     column_names=['key'], num_buckets=3)

        # # 创建新表
        # client.create_table('python-example', schema, partitioning)

    def insert(self, tbName, datas: List[Dict]):
        table = self.client.table(tbName)
        session = self.client.new_session()
        for data in datas:
            op = table.new_insert(data)
            session.apply(op)

        self.__flush(session)

    def upsert(self, tbName, datas):
        table = self.client.table(tbName)
        session = self.client.new_session()
        # 更新插入，即有则更新，无则插入
        for data in datas:
            op = table.new_upsert(data)
            session.apply(op)

        self.__flush(session)

    def update(self, tbName, datas):
        table = self.client.table(tbName)
        session = self.client.new_session()
        for data in datas:
            op = table.new_update(data)
            session.apply(op)

        self.__flush(session)

    def delete(self, tbName, datas):
        table = self.client.table(tbName)
        session = self.client.new_session()
        for data in datas:
            op = table.new_delete(data)
            session.apply(op)

        self.__flush(session)

    # def readAll(self,tbName):
    #     table = self.client.table(tbName)
    #     # 创建一个扫描，并增加一个python-example表的断言
    #     scanner = table.scanner()
    #     scanner.add_predicate(table['ts_val'] == datetime(2017, 1, 1))

    #     # 打开扫描仪并读取所有元组
    #     # 注: 这不适用于大扫描
    #     result = scanner.open().read_all_tuples()

    def __flush(self, session):
        try:
            session.flush()
        except kudu.KuduBadStatus as e:
            print(session.get_pending_errors())
