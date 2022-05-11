'''
Author: Logic
Date: 2022-04-21 10:43:15
LastEditTime: 2022-05-11 09:41:12
FilePath: \pyFuncs\myFunc\__init__.py
Description: 
'''
from .basic import configFunc, myClass, signFunc
from .conn import dbFunc

__all__ = ['basic', 'conn','graph']
__version__ = "1.0"
