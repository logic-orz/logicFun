import ctypes
import json
from functools import reduce as reduceWith
from typing import Any, Callable, Dict, List, Tuple, TypeVar

T = TypeVar('T')


class _PyObject(ctypes.Structure):
    class PyType(ctypes.Structure):
        pass

    s_size = ctypes.c_int64 if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_int32
    _fields_ = [
        ('ob_refcnt', s_size),
        ('ob_type', ctypes.POINTER(PyType)),
    ]


def sign(cls, funcName):  # * 功能注册装饰器,加在函数上,可以将函数注册到特定类
    """
    ? cls class类名
    ? funcName 注册的函数名称
    """
    def _(function):
        class SlotsProxy(_PyObject):
            _fields_ = [('dict', ctypes.POINTER(_PyObject))]

        name, target = cls.__name__, cls.__dict__
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


@sign(dict, 'vs')
def vs(self: dict) -> list:
    return list(self.values())


@sign(dict, 'ks')
def ks(self: dict) -> list:
    return list(self.keys())


@sign(dict, 'kvs')
def kvs(self: dict) -> list:
    re = []
    for k, v in self.items():
        re.append((k, v))
    return re


@sign(dict, 'del')
def delDictKV(self: dict, key: str) -> dict:
    del self[key]
    return self


@sign(dict, 'rename')
def reNameDictKey(self: dict, fkey: str, tkey: str) -> dict:
    if fkey in self.keys():
        v = self.pop(fkey)
        self[tkey] = v
    return self


@sign(dict, 'toStr')
def dictToStr(self) -> str:
    return json.dumps(self, ensure_ascii=False)

# * list


@sign(list, 'map')
def mapWith(self, __func: Callable[[Any], Any]):
    return list(map(__func, self))


@sign(list, 'flatMap')
def flatMapWith(self, __func: Callable[[Any], List[Any]]):
    res = []
    for ts in map(__func, self):
        if ts:
            res.extend(ts)
    return res


@sign(list, 'appendAll')
def appendAll(self: List[T], vs: List[T]) -> List[T]:
    self.extend(vs)
    return self


@sign(list, 'toSet')
def toSet(self):
    return set(self)


@sign(list, 'filter')
def filterWith(self, __func: Callable[[Any], bool]):
    return list(filter(__func, self))


@sign(list, 'distinct')
def distinct(self):
    return list(set(self))


@sign(list, 'groupByKey')
def groupByKey(self: List[Tuple[str, T]]) -> Dict[str, List[T]]:  # ? 聚合函数
    tmpMap: Dict[str, List[T]] = dict()
    for key, value in self:
        if key not in tmpMap:
            tmpMap[key] = []
        tmpMap[key].append(value)
    return tmpMap


@sign(list, 'toDict')
def tupleToDict(self: List[Tuple[str, T]]) -> Dict[str, T]:
    return dict(self)


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
        .map(lambda t: (t[0], reduceWith(__func, t[1])))\
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


@sign(list, 'split')
def splitList(self: List[Any], num: int = -1, size: int = -1):
    lens = len(self)
    if num != -1:
        re = [[] for i in range(0, num)]
        for i in range(0, lens):
            v = self[i]
            l = re[i % num]
            l.append(v)
    elif size != -1:
        re = []
        for i in range(0, lens, size):
            if i+size > lens:
                re.append(self[i:])
            else:
                re.append(self[i:i+size])
    return re


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


@sign(str, 'append')
def appendStr(self: str, s: str):
    return self + str(s)


@sign(str, 'toJson')
def toJson(self: str):
    return json.loads(self)
