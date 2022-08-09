'''
Author: Logic
Date: 2022-04-28 11:03:17
Description: 
'''
from functools import reduce as reduceWith
from typing import Dict, Callable, Any, List, Tuple, TypeVar
from .signClass import sign, T
import json


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


@sign(dict, 'toStr')
def dictToStr(self) -> str:
    return json.dumps(self, ensure_ascii=False)

# * list


@sign(list, 'map')
def mapWith(self, __func: Callable[[Any], Any]):
    return list(map(__func, self))

# * list


@sign(list, 'flatMap')
def flatMapWith(self, __func: Callable[[Any], List[Any]]):
    res = []
    for ts in map(__func, self):
        if ts:
            for t in ts:
                res.append(t)
    return res


@sign(list, 'appendAll')
def appendAll(self, vs: List[T]) -> List[T]:
    for v in vs:
        self.append(v)
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
