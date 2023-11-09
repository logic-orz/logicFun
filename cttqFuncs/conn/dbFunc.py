from typing import List, Dict
from ..basic.exClass import BaseClass
from ..basic.configFunc import getDict
import abc
import datetime
from pydantic import BaseModel
from ..exFunc import *


class DbConfig(BaseModel, BaseClass):
    """
    数据库连接配置对象
    """
    host: str = None
    port: int = None
    user: str = None
    pwd: str = None
    db: str = None
    address: str = None


class DbColumn(BaseModel, BaseClass):
    """
    字段信息对象
    """
    name: str = None
    type: str = None
    comment: str = None
    isId: bool = False


class DbFunc(metaclass=abc.ABCMeta):

    def __init__(self, config: DbConfig) -> None:
        pass

    @abc.abstractmethod
    def conn(self):
        # * 创建连接对象
        # TODO:子类实现
        raise Exception("子类实现创建连接对象方法")

    def execQuery(self, sql: str) -> List[dict]:
        conn = self.conn()
        cur = conn.cursor()
        cur.execute(sql)

        if cur.rowcount > 0:
            res_list = cur.fetchall()
        else:
            res_list = []

        cur.close()
        return res_list

    def execQueryIte(self, *sqls: str, batchSize: int = 1000):
        conn = self.conn()
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)
        i = 0
        while True:
            i += 1
            res_list = cur.fetchmany(batchSize)
            if not res_list:
                cur.close()
                return
            yield res_list

    def execSql(self, *sqls: str) -> None:
        conn = self.conn()
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)
        conn.commit()
        cur.close()

    def tables(self) -> List[str]:
        # * 获取所有数据表名
        # todo 子类实现
        raise Exception("方法未实现")

    def tableMeta(self, tbName: str) -> List[DbColumn]:
        """
        * 获取表的字段模式
        todo 子类实现
        """
        raise Exception("方法未实现")

    @classmethod
    def fix(cls, ns: str = None):
        if not ns:
            ns = cls.__name__.lower()
        return cls(DbConfig.build(getDict(ns)))


def createInsertSql(tbName: str, datas: List[dict]):

    keys = list(datas[0].keys())

    tmpValue = ''
    for data in datas:
        values = []
        for s in keys:
            if isinstance(data[s], str):
                vs = '"%s"' % (data[s].replace("\\", "\\\\").replace("\"", "\\\""))
            elif isinstance(data[s], datetime.datetime):
                vs = '"%s"' % (str(data[s]).replace("\"", "\\\""))
            elif isinstance(data[s], dict) or isinstance(data[s], list):
                vs = json.dumps(data[s], ensure_ascii=False)
            elif data[s] is None:
                vs = "null"
            else:  # 默认类型可以兼容
                vs = f"{data[s]}"

            values.append(vs)

        tmpValue = tmpValue + "({values}),".format(values=','.join(values))

    fields = '`, `'.join(keys)
    valueStr = tmpValue[:-1]
    sql = f'INSERT INTO {tbName}(`{fields}`) VALUES {valueStr}'
    return sql


def createInsertSqlForImpala(tbName: str, datas: List[dict], cols: List[DbColumn]):

    # 获取 字段名
    if len(datas) > 10:
        keys = datas[0:10].flatMap(lambda d: d.ks()).distinct()
    else:
        keys = datas.flatMap(lambda d: d.ks()).distinct()

    colType: Dict[str, str] = cols.map(lambda dc: (dc.name, dc.type)).toDict()

    tmpValue = ''
    for data in datas:
        values = []
        for s in keys:

            if s not in colType:  # 数据不在列内
                continue

            if colType[s].startsIn("string", "varchar", "text") and isinstance(data[s], str):
                vs = '"%s"' % (data[s].replace("\\", "\\\\").replace("\"", "\\\""))
            elif isinstance(data[s], datetime.datetime):
                vs = '"%s"' % (str(data[s]).replace("\"", "\\\""))
            elif colType[s].startsIn("string", "varchar", "text") and (isinstance(data[s], dict) or isinstance(data[s], list)):
                vs = json.dumps(data[s], ensure_ascii=False)
            elif colType[s].startswith('decimal'):  # impala decimal 类型需要强转
                vs = f"cast({data[s]} as {colType[s]} )"
            elif data[s] is None:
                vs = "null"
            else:  # 默认类型可以兼容
                vs = f"{data[s]}"

            values.append(vs)

        tmpValue = tmpValue + "({values}),".format(values=','.join(values))

    fields = '`, `'.join(keys)
    valueStr = tmpValue[:-1]

    sql = f'INSERT INTO {tbName}(`{fields}`) VALUES {valueStr}'
    return sql


def transData(datas: List[Dict], columns: List[DbColumn], z2e: bool = True):
    """_summary_
    数据字段名转换
    @param z2e: True中文转英文(默认) False:英文转中文
    不在范围内的字段,会被删除
    """
    for data in datas:
        fk_tk_types: Dict[str, Tuple[str, str]] = {}
        for col in columns:
            if z2e:
                fkey = col.comment
                tKey = col.name
            else:
                fkey = col.name
                tKey = col.comment
            fk_tk_types[fkey] = (tKey, col.type)

        for fkey in data.ks():

            v = data.pop(fkey)
            if fkey in fk_tk_types:
                tKey, vType = fk_tk_types[fkey]
                if vType.startswith('float') and isinstance(v, str):
                    v = float(v) if v != '' else None
                elif vType.startswith('int') and isinstance(v, str):
                    v = int(v) if v != '' else None
                elif vType.startswith('double') and isinstance(v, str):
                    v = float(v) if v != '' else None
                elif vType.startswith('decimal') and isinstance(v, str):
                    v = float(v) if v != '' else None
                elif vType.startswith('date') and isinstance(v, str):
                    v = v if v != '' else None
                elif vType.startswith('json') and isinstance(v, str):
                    v = json.loads(v) if v != '' and v.startsIn('{', '[') and v.endsIn('}', ']') else None
                data[tKey] = v
    return datas
