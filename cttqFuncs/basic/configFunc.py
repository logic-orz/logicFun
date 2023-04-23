import configparser
from typing import Dict
import os


    
_config = configparser.RawConfigParser()
# 设置大小写敏感
_config.optionxform=lambda option:option

configPaths = ['./resources/config.ini']
    
    
_sqlConfig = dict()
sqlPaths = ['./resources/config.sql']


def initFile():
    for configPath in configPaths:
        if os.path.exists(configPath):
            _config.read(configPath, encoding="utf-8-sig")
        else:
            print("配置文件不存在：%s " % configPath)
    
def initStr(dataStr):
    _config.read_string(dataStr)
        
def initSql(sqlPath: str):
    k = ''
    v = ''
    for line in open(sqlPath, 'r', encoding='UTF-8'):
        if line.endswith("\n"):
            line = line[:-1]
        if line.startswith("--") and line.endswith("--"):
            if k != '':
                _sqlConfig[k] = v
                k = ''
                v = ''

            k = line[2:-2].strip()
        elif not line.strip().startswith("--"):
            v = v+line+"\n"

    if k != '':
        _sqlConfig[k] = v
            
    

def getDict(nameSpace: str) -> Dict:
    if len(_config.sections())==0:
        initFile()
    '''
    Description: 以dict的方式返回配置
    '''
    tmpList = _config.items(nameSpace)
    
    return dict(tmpList)


def getValue(nameSpace: str, key: str) -> str:
    if len(_config.sections())==0:
        initFile()
    return _config.get(nameSpace, key)


def getSql(key: str) -> str:
    if len(_sqlConfig) == 0 :
        for sqlPath in sqlPaths:
            if os.path.exists(sqlPath):
                initSql(sqlPath)
            else:
                print("配置文件不存在：%s " % sqlPath)
    if key in _sqlConfig:
        return _sqlConfig[key]
    else:
        return ''
