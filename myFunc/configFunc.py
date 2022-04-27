'''
Author: your name
Date: 2022-04-19 15:42:25
LastEditTime: 2022-04-21 11:14:01
LastEditors: Please set LastEditors
Description: 配置读取工具类
FilePath: \py_func_manage\myFunc\configFunc.py
'''
import configparser

config = configparser.RawConfigParser()
config.read('./resources/config.ini', encoding="utf-8-sig")


def getDict(nameSpace):
    '''
    Description: 以dict的方式返回配置
    '''
    tmpList = config.items(nameSpace)
    re = {}
    for t in tmpList:
        re[t[0]] = t[1]

    return re


def getValue(nameSpace, key):
    return config.get(nameSpace, key)
