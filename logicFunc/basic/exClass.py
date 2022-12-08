from typing import Any, Callable, Dict, List, Tuple, TypeVar, Generic, Set
import json
import datetime
import decimal

T = TypeVar('T')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # 检查到是bytes类型的数据就转为str类型
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        # 检查到是datetime.datetime类型的数据就转为str类型
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, BaseClass):
            return obj.toDict()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class CommonException(Exception):
    def __init__(self, ErrorInfo):
        self.ErrorInfo = ErrorInfo

    def __str__(self):
        return self.ErrorInfo


class BaseClass:

    """
    * 基础父类,提供面向dict的转换方法
    """

    def build(self, _obj: Dict):
        if _obj:
            self.__dict__.update(_obj)
        return self

    def toDict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']

        return dict

    def toStr(self):
        return json.dumps(self.toDict(), cls=MyEncoder, ensure_ascii=False, indent=2)

    def __str__(self):
        return json.dumps(self.toDict(),  cls=MyEncoder, ensure_ascii=False, indent=2)

    def __repr__(self) -> str:
        return json.dumps(self.toDict(),  cls=MyEncoder, ensure_ascii=False, indent=2)


class IndexList(Generic[T]):
    """
     * 索引集合,主要面向检索，不建议修改数据
    """

    def __init__(self) -> None:
        #List[Tuple[T, List[str]]]
        self.data = list()
        self.index: Dict[str, Set[int]] = dict()

    def add(self, t: T, keys: List[str]):
        self.data.append((t, keys))
        num = self.data.__len__() - 1
        for key in keys:
            indexV = set()
            if key in self.index:
                indexV = self.index[key]
            indexV.add(num)
            self.index[key] = indexV

    def search(self, key: str):  # -> List[Tuple[int, T]]
        if key in self.index:
            numSet: set[int] = self.index[key]
            return numSet.toList()\
                .map(lambda n: (n, self.data[n][0]))
        return list()

    def remove(self, num: int):
        if not num in self.data:
            return
        tup = self.data[num]
        t = tup[0]
        keys = tup[1]
        self.data[num] = None

        for key in keys:
            if not key in self.index:
                continue
            numSet = self.index[key]
            numSet.remove(num)
            if len(numSet) == 0:
                del self.index[key]
            else:
                self.index[key] = numSet

    def vs(self) -> List[T]:
        return self.data.map(lambda t: t[0])


class StrBuild():  # * 面向长字符串多次需要拼接的场景

    def __init__(self) -> None:
        self.__strList__ = []

    def append(self, s):
        self.__strList__.append(str(s))
        return self

    def toStr(self):
        return ''.join(self.__strList__)


class Tree(Generic[T]):

    """
    * data:Dict[str:Tuple[str,T]] 对象字典:[key,[parentKey,value]]
    * path:Dict[str:set[str]] 路径层级关系
    """

    def __init__(self, name: str = '') -> None:
        self.name = name
        #Dict[str, Tuple[str, T]]
        self.data = dict()
        self.child: Dict[str, Set[str]] = dict()

    def add(self, key: str, v: T, parentKey: str = None):
        self.data[key] = (parentKey, v)

        children = set()
        if parentKey in self.child:
            children = self.child[parentKey]

        children.add(key)
        self.child[parentKey] = children

    def get(self, key: str) -> T:
        if key in self.data:
            return self.data[key][1]
        return None

    def delete(self, key: str):
        childKeys = {key}

        tmpKeys: List[str] = list()
        tmpKeys.append(key)

        while len(tmpKeys) > 0:
            ts = list()
            for tmp in tmpKeys:
                ts.appendAll(self.getChildrenKeys(tmp))

            tmpKeys.clear()
            tmpKeys.appendAll(ts)

        pk = self.data[key][0]
        ps = self.child[pk]
        ps.remove(key)
        if len(ps) == 0:
            del self.child[pk]
        for k in childKeys:
            del self.child[k]
            del self.data[k]

    def getChildren(self, key: str) -> List[T]:
        if key in self.child:
            childKeys: set[int] = self.child[key]
            return childKeys.toList().map(lambda k: self.data[k][1])
        return []

    def getChildrenKeys(self, key: str) -> List[str]:
        if key in self.child:
            return self.child[key].toList()
        return []

    def getParent(self, key: str) -> T:
        if key in self.data:
            pk = self.data[key][0]
            return self.data[pk][1]
        return None

    def values(self):
        return self.data.vs().map(lambda t: t[1])


class Matrix():
    """
    x:横坐标
    y:纵坐标
    row: 行
    column: 列
    """

    def __init__(
        self,
        rowL: int = 1,
        colL: int = 1,
        initValue: Any = '',
    ) -> None:

        self.matrix = list(range(0, rowL))\
            .map(lambda i: list(range(0, colL))
                 .map(lambda j: initValue))

    @property
    def rowL(self):
        return len(self.matrix)

    @property
    def colL(self):
        return len(self.matrix[0])

    def cell(self, rowN: int, colN: int):
        return self.matrix[rowN][colN]

    def setCell(self, colN, rowN, v: Any):
        self.matrix[rowN][colN] = v

    def row(self, rowN: int) -> List[Any]:
        return self.matrix[rowN]

    def rows(self, rowNs: List[int]):
        return rowNs.map(lambda rowN: self.matrix[rowN])

    def setRow(self, rowN: int, v: List[Any]):
        self.matrix[rowN] = v

    def column(self, colN: int) -> List[Any]:
        return self.matrix.map(lambda arr: arr[colN])

    def columns(self, colNs: List[int]):
        return self.matrix.map(lambda arr: colNs.map(lambda colN: arr[colN]))

    def setColumn(self, colN: int, v: List[Any]):
        for i in range(0, len(v)):
            self.matrix[i][colN] = v[i]

    def addRow(self, v: List[Any], index: int = None):
        if not index:
            self.matrix.append(v)
        else:
            self.matrix = self.matrix[0:index].append(v) + self.matrix[index:]

    def delRow(self, index: int):
        self.matrix = self.matrix[0:index] + self.matrix[index + 1:]

    def delColumn(self, index: int):
        for i in range(0, self.rowN):
            t = self.matrix[i]
            t = t[0:index] + t[index + 1:]
            self.matrix[i] = t

    def addColumn(self, v: List[Any], index: int = None):
        if not index:
            for i in range(0, self.rowN):
                self.matrix[i].append(v[i])
        else:
            for i in range(0, self.rowN):
                t = self.matrix[i]
                t = t[0:index].append(v[i]) + t[index:]
                self.matrix[i] = t

   

def matrixCut(a: Matrix, colL, rowL, x=0, y=0):
    tmpMatrix = Matrix(rowL, colL, None)

    for i in range(x, x + colL):
        for j in range(y, y + rowL):
            tmpMatrix.setCell(i - x, j - y, a.cell(i, j))

    return tmpMatrix


def matrixTranspose(a: Matrix):
    tmpMatrix = Matrix(a.colL, a.rowL, None)

    for i in range(0, a.colL):
        for j in range(0, a.rowL):
            tmpMatrix.setCell(j, i, a.cell(i, j))

    return tmpMatrix


def matrixMultiply(a: Matrix, b: Matrix):
    # a: m * s
    # b: s * n
    # c: m * n
    tmpM = Matrix(a.rowL, b.colL, initValue=0.0)
    for m in range(0, a.rowL):
        for n in range(0, b.colL):
            r = a.row(m)
            c = b.column(n)
            v = list(zip(r, c)).map(lambda t: t[0] * t[1]).doSelf(sum)
            tmpM.setCell(x=n, y=m, v=v)

    return tmpM


def matrixCal(a: Matrix, func: Callable[[Any], Any]):
    tmpM = Matrix(a.rowL, a.colL, initValue=0.0)
    tmpM.matrix = tmpM.map(lambda row: row.map(lambda v: func(v)))
    return tmpM


class Row(BaseClass):

    def __init__(self, headers, values=None) -> None:
        self.headers = headers
        if values:
            self.values = values
        else:
            self.values = list(range(0, len(headers))).map(lambda i: None)

    def getCell(self, key):
        return self.values[self.headers.index(key)]

    def setCell(self, key, value):
        self.values[self.headers.index(key)] = value
        return self

    @property
    def rowDict(self):
        return dict(zip(self.headers, self.values))


class RowTable(BaseClass):

    def __init__(self, headers: List[str], title: str = '') -> None:
        self.title = title
        self.rows: List[Row] = []
        self.headers = headers

    def addRow(self, datas: List[Any]):
        self.rows.append(Row(self.headers, datas))

    @property
    def rowN(self):
        return len(self.rows)

    def allRowValues(self):
        return self.rows.map(lambda row: row.values)
