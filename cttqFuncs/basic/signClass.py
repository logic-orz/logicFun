'''
Author: Logic
Date: 2022-05-17 14:24:15
LastEditTime: 2022-05-19 09:45:30
Description: 
'''
import json
from typing import Callable,Any, Dict


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
