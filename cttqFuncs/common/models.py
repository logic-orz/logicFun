'''
Author: Logic
Date: 2022-09-26 19:34:17
LastEditTime: 2022-09-26 19:34:17
Description: 
'''
import json
from typing import Any, Callable, List, Dict, Tuple
import cttqFuncs.basic.exFunc
from cttqFuncs.common.dataShow import createKTableWithMatrix
from cttqFuncs.basic.exClass import BaseClass


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

    def toStr(self):

        return createKTableWithMatrix(
            headers=['-'] + list(range(0, self.columnN)),
            datas=list(zip(list(range(0, self.rowN)),
                           self.matrix)).map(lambda t: [str(t[0])] + t[1]))

    def tbStr(self, colKs: List[str], rowKs: List[str]):
        return createKTableWithMatrix(
            headers=['-'] + colKs,
            datas=list(zip(rowKs,
                           self.matrix)).map(lambda t: [str(t[0])] + t[1]),
        )


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

    def toStr(self):
        return createKTableWithMatrix(headers=self.headers,
                                      datas=self.allRowValues(),
                                      title=self.title)
