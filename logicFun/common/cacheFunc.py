from cacheout import MRUCache
from typing import Dict
_caches:Dict[str,MRUCache]={}

class cachePut(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """
<<<<<<< HEAD:logicFun/common/cacheFunc.py
    def __init__(self, key: str,expire:int=-1):
        self.key = key
        if key not in _caches:
            _caches[key]=MRUCache(ttl=expire)
=======
    def __init__(self, ns: str='default',expire:int=0):
        self.ns = ns
        if ns not in _caches:
            _caches[ns]=MRUCache(ttl=expire)
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/cacheFunc.py

    def __call__(self, __func):  # 接受函数

        def wrapper(*args, **kwargs):
            k= list(args) + list(kwargs.values())
            k=tuple(map(lambda o:str(o),k))
<<<<<<< HEAD:logicFun/common/cacheFunc.py
            cache=_caches[self.key]
=======
            cache=_caches[self.ns]
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/cacheFunc.py
            
            re=__func(*args, **kwargs)
            cache.add(k,re)
            return re
        
        
        return wrapper  # 返回函数



class cacheable(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """
<<<<<<< HEAD:logicFun/common/cacheFunc.py
    def __init__(self, key: str,expire:int=-1):
        self.key = key
        if key not in _caches:
            _caches[key]=MRUCache(ttl=expire)
=======
    def __init__(self, ns: str='default',expire:int=0):
        self.ns = ns
        if ns not in _caches:
            _caches[ns]=MRUCache(ttl=expire)
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/cacheFunc.py

    def __call__(self, __func):  #  

        def wrapper(*args, **kwargs):
            k= list(args) + list(kwargs.values())
            k=tuple(map(lambda o:str(o),k))
<<<<<<< HEAD:logicFun/common/cacheFunc.py
            cache=_caches[self.key]
=======
            cache=_caches[self.ns]
>>>>>>> cc557459720bb2265615b0b0d7cb7dd3eb02e129:cttqFuncs/common/cacheFunc.py
            
            cre=cache.get(k,None)
            if cre:
                return cre
            re=__func(*args, **kwargs)
            cache.add(k,re)
            return re
        
        
        return wrapper  # 返回函数