'''
Author: Logic
Date: 2022-04-26 08:55:29
LastEditTime: 2022-04-26 18:58:19
FilePath: \py_func_manage\myFunc\myClass.py
Description:
'''
from functools import reduce
from typing import Dict, MutableSequence, Generic, Callable, Any, List, Tuple
import json
import operator
import ctypes

from sqlalchemy import false


class PyObject(ctypes.Structure):
    class PyType(ctypes.Structure):
        pass

    ssize = ctypes.c_int64 if ctypes.sizeof(
        ctypes.c_void_p) == 8 else ctypes.c_int32
    _fields_ = [
        ('ob_refcnt', ssize),
        ('ob_type', ctypes.POINTER(PyType)),
    ]


def sign(clazz, funcName):
    """
    * 功能注册装饰器
    * 加在函数上,可以将函数注册到特定类
    ? clazz class类名
    ? funcName 注册的函数名称
    """
    def _(function):
        class SlotsProxy(PyObject):
            _fields_ = [('dict', ctypes.POINTER(PyObject))]

        name, target = clazz.__name__, clazz.__dict__
        proxy_dict = SlotsProxy.from_address(id(target))
        namespace = {}
        ctypes.pythonapi.PyDict_SetItem(
            ctypes.py_object(namespace),
            ctypes.py_object(name),
            proxy_dict.dict,
        )
        namespace[name][funcName] = function

    return _

# * 函数注册

# * dict


@sign(dict, 'myValues')
def myValues(self: dict) -> list:
    return list(self.values())


@sign(dict, 'myKeys')
def myKeys(self: dict) -> list:
    return list(self.keys())


@sign(dict, 'kvs')
def kvs(self: dict) -> list:
    re = []
    for k, v in self.items():
        re.append((k, v))
    return re


# * list


@sign(list, 'mapWith')
def mapWith(self, __func: Callable[[Any], Any]):
    return list(map(__func, self))


@sign(list, 'toSet')
def toSet(self):
    return set(self)


@sign(list, 'filterWith')
def filterWith(self, __func: Callable[[Any], Any]):
    return list(filter(__func, self))


@sign(list, 'groupByKey')
def groupByKey(self: List[Tuple[str, Any]]) -> Dict[str, List[Any]]:  # ? 聚合函数
    tmpMap = dict()
    for data in self:
        key = data[0]
        value = data[1]
        valueList = []
        if key in tmpMap:
            valueList = tmpMap[key]
        valueList.append(value)
        tmpMap[key] = valueList

    return tmpMap


@sign(list, 'tupleToDict')
def tupleToDict(self: List[Tuple[str, Any]]):
    re = dict()
    for t in self:
        re[t[0]] = t[1]

    return re


@sign(list, 'reduceWith')
def reduceWith(self, __func):
    return reduce(__func, self)


@sign(list, 'reduceByKey')
def reduceByKey(self: List[Tuple[str, Any]], __func: Callable[[Any], Any]):
    re = self.groupByKey()\
        .kvs()\
        .mapWith(lambda t: (t[0], t[1].reduceWith(__func)))\
        .tupleToDict()
    return re

@sign(list, 'foreach')
def foreach(self, __func):
    for t in self:
        __func(t)

# * set


@sign(set, 'toList')
def toList(self):
    return list(self)


# * str


@sign(str, 'startsIn')
def startsIn(self: str, *keys):
    for s in keys:
        if self.startswith(s):
            return True
    return False


@sign(str, 'endsIn')
def endsIn(self: str, *keys):
    for s in keys:
        if self.endswith(s):
            return True
    return False


class BaseClass:

    def fromDict(self, _obj):
        if _obj:
            self.__dict__.update(_obj)
        return self

    def toDict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict

    def __repr__(self) -> str:
        return json.dumps(self.toDict(), ensure_ascii=False)

# 如果想要代码提示,可以使用继承的子类
