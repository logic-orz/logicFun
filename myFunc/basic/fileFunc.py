'''
Author: Logic
Date: 2022-04-29 19:10:30
LastEditTime: 2022-05-09 15:29:47
FilePath: \pyFuncs\myFunc\basic\fileFunc.py
Description: 
'''
import os
from typing import List
from myFunc.basic.myClass import StrBuild
from myFunc.basic.signFunc import *


def deleteFile(path: str):
    if os.path.exists(path):
        os.remove(path)


def readLines(path: str, encoding='UTF-8') -> List[str]:
    re = []
    for line in open(path, 'r', encoding):
        re.append(line)
    return re


def readStr(path: str, encoding='UTF-8') -> str:
    sb = StrBuild()
    for line in open(path, 'r', encoding):
        sb.append(line)
    return sb.toStr()


def writeAppend(path: str, lines: List[str], encoding='UTF-8'):
    with open(path, 'a', encoding) as f:
        f.writelines(lines)
