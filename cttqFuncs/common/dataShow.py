'''
Author: Logic
Date: 2022-09-08 11:03:51
LastEditTime: 2022-09-26 19:34:49
Description: 
'''
from prettytable import PrettyTable
from prettytable import ALL as ALL
import cttqFuncs.basic.exFunc
from typing import List, Dict
from textwrap import fill
from IPython.display import display


def showKTable(datas: List[Dict], title: str = '', fillWidth=100) -> PrettyTable:
    '''
    将数据展示成宽表
    传入list
    '''
    x = PrettyTable()
    x.title = title
    ks: List[str] = datas.flatMap(lambda d: d.ks()).toSet().toList()
    x.field_names = ks
    for data in datas:
        x.add_row(ks.map(lambda k: fill(
            str(data[k]), fillWidth) if k in data else ''))
    display(x)
    return x


def showKTableWithMatrix(headers: List[str], datas: List[list], title: str = '', fillWidth=100) -> PrettyTable:
    '''
    将数据展示成宽表
    传入 表头和数据矩阵
    '''
    x = PrettyTable()
    x.title = title
    x.field_names = headers
    for data in datas:
        x.add_row(data.map(lambda t: fill(str(t), fillWidth) if t else ''))
    display(x)
    return x


def createKTableWithMatrix(headers: List[str], datas: List[list], title: str = '', fillWidth=100) -> str:
    '''
    将数据展示成宽表
    传入 表头和数据矩阵
    '''
    x = PrettyTable()
    x.title = title
    x.field_names = headers
    for data in datas:
        x.add_row(data.map(lambda t: fill(str(t), fillWidth) if t else ''))
    return '\n'+str(x)

def showZTable(data: Dict, title: str = '', fillWidth=100) -> PrettyTable:
    '''
    将数据展示成窄表
    '''
    x = PrettyTable(hrules=ALL)
    x.title = title
    x.field_names = ['name', 'value']
    data.kvs().foreach(lambda kv: x.add_row(
        [kv[0], fill(str(kv[1]), fillWidth)]))
    display(x)
    return x
