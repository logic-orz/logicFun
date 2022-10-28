'''
Author: Logic
Date: 2022-05-17 14:24:15
LastEditTime: 2022-05-19 09:45:30
Description: 
'''


from typing import Dict, Callable, Any, List, Tuple, TypeVar
import ctypes
import json
from functools import reduce as reduceWith

T = TypeVar('T')


class PyObject(ctypes.Structure):
    class PyType(ctypes.Structure):
        pass

    ssize = ctypes.c_int64 if ctypes.sizeof(
        ctypes.c_void_p) == 8 else ctypes.c_int32
    _fields_ = [
        ('ob_refcnt', ssize),
        ('ob_type', ctypes.POINTER(PyType)),
    ]


def sign(clazz, funcName):  # * 功能注册装饰器,加在函数上,可以将函数注册到特定类
    """
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


class doJoin(object):
    """
    * 并行函数，参数和被装饰函数的参数保持一致
    * 执行逻辑与被装饰内容无关，只为了执行被装饰函数时，并行执行某个方法
    * 当前是在函数执行之前执行
    """

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(self, __func):  # 接受函数
        def wrapper(*args, **kwargs):
            self.func(*args, **kwargs)
            return __func(*args, **kwargs)
        return wrapper  # 返回函数


class doBefore(object):
    """
    * 前置函数,参数和被装饰函数的参数保持一致
    * 前置函数返回值,作为被装饰函数的输入
    * 为了避免 got multiple values for argument 错误,需要返回的参数,请以kwargs的形式传入
    * 返回参数会更新kwargs,所以请以字典形式返回变更的参数
    """

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(self, __func):  # 接受函数
        def wrapper(*args, **kwargs):
            kwargsT = self.func(*args, **kwargs)
            kwargs.update(kwargsT)
            return __func(*args, **kwargs)

        return wrapper  # 返回函数


class doAfter(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __call__(self, __func):  # 接受函数
        def wrapper(*args, **kwargs):
            res = __func(*args, **kwargs)
            return self.func(res)

        return wrapper  # 返回函数


# def parInit(cls):
#     ps=list(cls.__bases__)
#     def addInit(*args, **kwargs):
#         for p in ps:
#             p.__init__(args[0])
#             print(p.__name__)
#         cls.__init__(*args, **kwargs)
#     cls.__init__ = addInit
#     return cls


def toDict(cls):
    def func(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']

        return dict

    cls.toDict = func
    return cls


def toStr(cls):
    def func(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return json.dumps(dict, ensure_ascii=False)

    cls.toStr = func
    cls.__repr__ = func

    return cls


def build(cls):
    def func(self, _obj: Dict):
        if _obj:
            self.__dict__.update(_obj)
        return self

    cls.build = func
    return cls


class ZList(list):

    def map(self, __func: Callable[[Any], Any]):
        return ZList(map(__func, self))

    def flatMap(self, __func: Callable[[Any], List[Any]]):
        res = []
        for ts in map(__func, self):
            if ts:
                for t in ts:
                    res.append(t)
        return res

    def appendAll(self, vs: List[T]) -> List[T]:
        for v in vs:
            self.append(v)
        return self

    def toSet(self):
        return set(self)

    def filter(self, __func: Callable[[Any], bool]):
        return list(filter(__func, self))


@sign(list, 'distinct')
def distinct(self):
    return list(set(self))


@sign(list, 'groupByKey')
def groupByKey(self: List[Tuple[str, T]]) -> Dict[str, List[T]]:  # ? 聚合函数
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


@sign(list, 'toDict')
def tupleToDict(self: List[Tuple[str, T]]) -> Dict[str, T]:
    re = dict()
    for t in self:
        re[t[0]] = t[1]

    return re


@sign(list, 'reduce')
def reduce(self, __func):
    return reduceWith(__func, self)


@sign(list, 'doSelf')
def doSelf(self, __func):
    return __func(self)


@sign(list, 'sum')
def sumWith(self: List):
    return sum(self)


@sign(list, 'reduceByKey')
def reduceByKey(self: List[Tuple[str, T]], __func: Callable[[T], T]) -> Dict[str, T]:
    re = self.groupByKey()\
        .kvs()\
        .map(lambda t: (t[0], t[1].reduce(__func)))\
        .toDict()
    return re


@sign(list, 'foreach')
def foreach(self, __func):
    for t in self:
        __func(t)
    return self


@sign(list, 'toStr')
def listToStr(self) -> str:
    return json.dumps(self, ensure_ascii=False)


@sign(list, 'isEmpty')
def listIsEmpty(self: List) -> bool:
    return len(self) == 0


@sign(list, 'sortBy')
def sortBy(self: List, key, reverse=False) -> list:
    self.sort(key=key, reverse=reverse)
    return self
