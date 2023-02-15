'''
Author: Logic
Date: 2022-09-08 11:03:51
LastEditTime: 2022-09-26 19:34:49
Description:  如果出现  type object 'UserString' has no attribute 'append' 等 错误,需要改变引用顺序,保持dataShow在exFuncs之前引入
'''
from prettytable import PrettyTable
from prettytable import ALL as ALL

from typing import List, Dict
from textwrap import fill
from IPython.display import display
from ..basic.exFunc import *

def showKTable(datas: List[Dict], title: str = '', fillWidth=100, show=True) -> str:
    '''
    将数据展示成宽表
    传入list
    '''
    if len(datas)==0:
        return ''
    x = PrettyTable()
    x.title = title
    ks: List[str] = datas.flatMap(lambda d: d.ks()).toSet().toList()
    x.field_names = ks
    for data in datas:
        x.add_row(ks.map(lambda k: fill(
            str(data[k]), fillWidth) if k in data else ''))
    if show:
        display(x)
    return '\n'+str(x)


def showKTableWithMatrix(headers: List[str], datas: List[list], title: str = '', fillWidth=100, show=True) -> str:
    '''
    将数据展示成宽表
    传入 表头和数据矩阵
    '''
    if len(datas)==0:
        return ''
    x = PrettyTable()
    x.title = title
    x.field_names = headers
    for data in datas:
        x.add_row(data.map(lambda t: fill(str(t), fillWidth) if t else ''))
    if show:
        display(x)
    return '\n'+str(x)


def showZTable(data: Dict, title: str = '', fillWidth=100, show=True) -> str:
    '''
    将数据展示成窄表
    '''
    if len(data.keys())==0:
        return ''
    x = PrettyTable(hrules=ALL)
    x.title = title
    x.field_names = ['name', 'value']
    data.kvs().foreach(lambda kv: x.add_row(
        [kv[0], fill(str(kv[1]), fillWidth)]))
    if show:
        display(x)
    return '\n'+str(x)
