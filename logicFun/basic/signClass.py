import asyncio
import json
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Callable, Dict


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


_threadPool = ThreadPoolExecutor(max_workers=10)


class runThread(object):
    """
    * 转换为异步任务
    """

    def __init__(self):
        pass

    def __call__(self, _func):  # 接受函数
        def callback(future: Future):
            print(f'future state: {future._state}')

        def wrapper(*args, **kwargs):
            future = _threadPool.submit(_func, *args, **kwargs)
            future.add_done_callback(callback)

        return wrapper  # 返回函数


_processPool = ProcessPoolExecutor(max_workers=10)


class runProcess(object):
    """
    * 转换为异步任务
    """

    def __init__(self):
        pass

    def __call__(self, _func):  # 接受函数
        def callback(future: Future):
            print(f'future state: {future._state}')

        def wrapper(*args, **kwargs):
            future = _processPool.submit(_func, *args, **kwargs)
            future.add_done_callback(callback)
            return

        return wrapper  # 返回函数


class runLoop(object):
    """
    * 转换为异步任务
    """

    def __init__(self, loop=None):
        if not loop:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

    def __call__(self, _func):  # 接受函数

        def wrapper(*args, **kwargs):
            self.loop.run_in_executor(None, _func, *args, **kwargs)
            return

        return wrapper  # 返回函数
