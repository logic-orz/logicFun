from cacheout import MRUCache
from typing import Dict
_caches:Dict[str,MRUCache]={}

class cacheput(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """
    def __init__(self, key: str,expire:int=-1):
        self.key = key
        if key not in _caches:
            _caches[key]=MRUCache(ttl=expire)

    def __call__(self, __func):  # 接受函数

        def wrapper(*args, **kwargs):
            k= list(args) + list(kwargs.values())
            k=tuple(map(lambda o:str(o),k))
            cache=_caches[self.key]
            
            re=__func(*args, **kwargs)
            cache.add(k,re)
            return re
        
        
        return wrapper  # 返回函数



class cacheable(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """
    def __init__(self, key: str,expire:int=-1):
        self.key = key
        if key not in _caches:
            _caches[key]=MRUCache(ttl=expire)

    def __call__(self, __func):  #  

        def wrapper(*args, **kwargs):
            k= list(args) + list(kwargs.values())
            k=tuple(map(lambda o:str(o),k))
            cache=_caches[self.key]
            
            cre=cache.get(k,None)
            if cre:
                return cre
            re=__func(*args, **kwargs)
            cache.add(k,re)
            return re
        
        
        return wrapper  # 返回函数