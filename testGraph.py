'''
Author: Logic
Date: 2022-04-27 16:00:35
LastEditTime: 2022-04-29 09:25:00
FilePath: \pyFuncs\testGraph.py
Description: 
'''
from myFunc.conn.impalaFunc import Impala

from myFunc.basic.myClass import BaseClass
from myFunc.basic.configFunc import getValue, configPath
import myFunc.basic.signFunc

from graph.beans import *
from typing import Set, Tuple


class TmpC(BaseClass):
    def __init__(self) -> None:

        self.cmpy_nm = None
        self.dept01_nm = None
        self.dept02_nm = None
        self.dept03_nm = None
        self.dept04_nm = None
        self.dept05_nm = None
        self.dept06_nm = None
        self.dept07_nm = None


graph = Graph()
Impala = Impala.fixedImpala()

sql = getValue('sql', 'deptSetSql')
datas: List[TmpC] = Impala.execQuery(sql).map(lambda d: TmpC().build(d))

tSet: Set[Tuple[str, str]] = set()


for tc in datas:
    # if tc.dept07_nm != tc.dept06_nm:
    #     tSet.add((tc.dept06_nm, tc.dept07_nm))
    # if tc.dept05_nm != tc.dept06_nm:
    #     tSet.add((tc.dept05_nm, tc.dept06_nm))
    # if tc.dept04_nm != tc.dept05_nm:
    #     tSet.add((tc.dept04_nm, tc.dept05_nm))
    # if tc.dept03_nm != tc.dept04_nm:
    #     tSet.add((tc.dept04_nm, tc.dept04_nm))
    # if tc.dept02_nm != tc.dept03_nm:
    #     tSet.add((tc.dept03_nm, tc.dept03_nm))
    if tc.dept01_nm != tc.dept02_nm:
        tSet.add((tc.dept01_nm, tc.dept02_nm))
    if tc.cmpy_nm != tc.dept01_nm:
        tSet.add((tc.cmpy_nm, tc.dept01_nm))

ss = tSet.toList().map(lambda t: Edge().build(t[0], t[1]))
graph.edges.appendAll(ss)
