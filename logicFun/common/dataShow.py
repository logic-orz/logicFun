<<<<<<< HEAD:logicFun/common/dataShow.py
from prettytable import PrettyTable
from prettytable import ALL as ALL

from typing import List, Dict
=======
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/dataShow.py
from textwrap import fill
from typing import Dict, List

from IPython.display import display
<<<<<<< HEAD:logicFun/common/dataShow.py
from ..exFunc import *

def showKTable(datas: List[Dict], title: str = '', fillWidth=100, show=True) -> str:
=======
from prettytable import ALL as ALL
from prettytable import PrettyTable

from ..exFunc import *


def showKTable(datas: List[Dict], title: str = '', headers: List[str] = None, fillWidth=100, show=True) -> str:
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/dataShow.py
    """
    将数据展示成宽表
    传入list
    @error 如果出现  type object 'UserString' has no attribute 'append' 等 错误,需要改变引用顺序,保持dataShow在exFunc之前引入
    """
<<<<<<< HEAD:logicFun/common/dataShow.py
    if len(datas)==0:
=======
    if len(datas) == 0:
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/dataShow.py
        return ''
    x = PrettyTable()
    x.title = title
    if not headers:
        headers: List[str] = datas.flatMap(lambda d: d.ks()).toSet().toList()
    x.field_names = headers
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
    @error 如果出现  type object 'UserString' has no attribute 'append' 等 错误,需要改变引用顺序,保持dataShow在exFunc之前引入
    '''
<<<<<<< HEAD:logicFun/common/dataShow.py
    if len(datas)==0:
=======
    if len(datas) == 0:
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/dataShow.py
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
    @error 如果出现  type object 'UserString' has no attribute 'append' 等 错误,需要改变引用顺序,保持dataShow在exFunc之前引入
    '''
<<<<<<< HEAD:logicFun/common/dataShow.py
    if len(data.keys())==0:
=======
    if len(data.keys()) == 0:
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/dataShow.py
        return ''
    x = PrettyTable(hrules=ALL)
    x.title = title
    x.field_names = ['name', 'value']
    data.kvs().foreach(lambda kv: x.add_row(
        [kv[0], fill(str(kv[1]), fillWidth)]))
    if show:
        display(x)
    return '\n'+str(x)
