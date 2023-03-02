from ..basic.exFunc import *
from typing import Dict,List,Tuple

def spaceCalWithOrderAdd(datas:List[Tuple[str,int]],limitSize:int)->List[Tuple[List[str],int]]:
    '''
    只做空间计算,不计较价值
    顺序添加
    @param  data: List[Tuple[物品名称,物品体积]]
    @param  size: 背包大小 
    @return     : List[Tuple[List[物品名称],物品总体积]]
    '''
    groups:List[Tuple[List[str],int]]=[]
    
    tmpGroupNames=[]
    tmpGroupSize=0
    for name,size in datas:
        if tmpGroupSize+size > limitSize: # 判断是否超出空间限制
            groups.append((tmpGroupNames.copy(),tmpGroupSize))
            tmpGroupNames.clear()
            tmpGroupSize=0
            
        tmpGroupNames.append(name)
        tmpGroupSize+=size
        
    if tmpGroupSize>0 or len(tmpGroupNames)>0:
        groups.append((tmpGroupNames.copy(),tmpGroupSize))
        
    return groups
    
    
    
    
    
    
    
    