'''
Author: Logic
Date: 2022-04-19 15:42:25
LastEditTime: 2022-05-17 10:04:43
Description: 配置读取工具类
FilePath: \pyFuncs\myFunc\basic\configFunc.py
'''
import configparser
from re import I
from typing import Dict
import os

config = None
configPath = './resources/config.ini'


def initConfig():
    global config
    config = configparser.RawConfigParser()
    config.read(configPath, encoding="utf-8-sig")


def getDict(nameSpace: str) -> Dict:
    if config is None:
        initConfig()
    '''
    Description: 以dict的方式返回配置
    '''
    tmpList = config.items(nameSpace)
    re = {}
    for t in tmpList:
        re[t[0]] = t[1]

    return re


def getValue(nameSpace: str, key: str) -> str:
    if config is None:
        initConfig()
    return config.get(nameSpace, key)


sqlConfig = dict()
sqlPaths = ['./resources/config.sql']


def initSqlConfig(sqlPath: str):

    k = ''
    v = ''
    for line in open(sqlPath, 'r', encoding='UTF-8'):
        if line.endswith("\n"):
            line = line[:-1]
        if line.startswith("--") and line.endswith("--"):
            if k != '':
                sqlConfig[k] = v
                k = ''
                v = ''

            k = line[2:-2].strip()
        elif not line.strip().startswith("--"):
            v = v+line+"\n"

    if k != '':
        sqlConfig[k] = v


def getSql(key: str) -> str:
    if len(sqlConfig) == 0:
        for s in sqlPaths:
            initSqlConfig(s)
    if key in sqlConfig:
        return sqlConfig[key]
    else:
        return ''
