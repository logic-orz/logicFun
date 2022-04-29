'''
Author: Logic
Date: 2022-04-21 10:43:15
LastEditTime: 2022-04-28 13:36:21
FilePath: \pyFuncs\myFunc\__init__.py
Description: 
'''
from .basic import configFunc, myClass, signFunc
from .conn import dbFunc, impalaFunc, redisFunc, mysqlFunc

__all__ = ['basic', 'conn']
__version__ = "1.0"
