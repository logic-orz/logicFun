'''
Author: Logic
Date: 2022-04-19 15:42:25
LastEditTime: 2022-05-19 15:41:09
Description: 配置读取工具类
'''
import configparser
from typing import Dict
import os

_config = None
configPaths = ['./resources/config.ini']


def initConfig():
    global _config
    _config = configparser.RawConfigParser()
    for configPath in configPaths:
        _config.read(configPath, encoding="utf-8-sig")


def getDict(nameSpace: str) -> Dict:
    if _config is None:
        initConfig()
    '''
    Description: 以dict的方式返回配置
    '''
    tmpList = _config.items(nameSpace)
    re = {}
    for t in tmpList:
        re[t[0]] = t[1]

    return re


def getValue(nameSpace: str, key: str) -> str:
    if _config is None:
        initConfig()
    return _config.get(nameSpace, key)


_sqlConfig = dict()
sqlPaths = ['./resources/config.sql']


def initSqlConfig(sqlPath: str):

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


def getSql(key: str, hotLoading: bool = False) -> str:
    if len(_sqlConfig) == 0 or hotLoading:
        for s in sqlPaths:
            initSqlConfig(s)
    if key in _sqlConfig:
        return _sqlConfig[key]
    else:
        return ''
