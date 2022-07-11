from prettytable import PrettyTable
from prettytable import ALL as ALL
import cttqFuncs.basic.exFunc 
from typing import List, Dict
from textwrap import fill
from IPython.display import display


def showKTable(datas: List[Dict], title: str = ''):
    x = PrettyTable()
    x.title = title
    ks: List[str] = datas.flatMap(lambda d: d.ks()).toSet().toList()
    x.field_names = ks
    for data in datas:
        x.add_row(ks.map(lambda k: str(data[k]) if k in data else ''))
    display(x)


def showZTable(data: Dict, title: str = '', fillWidth=100):
    x = PrettyTable(hrules=ALL)
    x.title = title
    x.field_names = ['column', 'value']
    data.kvs().foreach(lambda kv: x.add_row(
        [kv[0], fill(str(kv[1]), fillWidth)]))
    display(x)


