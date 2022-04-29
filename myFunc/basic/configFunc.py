'''
Author: Logic
Date: 2022-04-19 15:42:25
LastEditTime: 2022-04-29 09:02:09
Description: 配置读取工具类
FilePath: \pyFuncs\myFunc\basic\configFunc.py
'''
import configparser
from typing import Dict

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
