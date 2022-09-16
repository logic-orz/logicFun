'''
Author: Logic
Date: 2022-04-29 19:10:30
LastEditTime: 2022-05-19 15:02:48
FilePath: \pyFuncs\cttqFuncs\basic\fileFunc.py
Description: 
'''
import os
from .exClass import StrBuild
from .exFunc import *
import shutil
import requests


def deleteFile(path: str):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))


def listFile(path: str):
    if os.path.exists(path):
        return os.listdir(path).map(lambda s: path+"/"+s).filter(lambda p: os.path.isfile(p))
    return list()


def listDir(path: str):
    if os.path.exists(path):
        return os.listdir(path).map(lambda s: path+"/"+s).filter(lambda p: os.path.isdir(p))
    return list()


def readLines(path: str, encoding='UTF-8'):
    re: List[str] = list()
    for line in open(path, 'r', encoding=encoding):
        re.append(line)
    return re


def readStr(path: str, encoding='UTF-8') -> str:
    sb = StrBuild()
    for line in open(path, 'r', encoding=encoding):
        sb.append(line)
    return sb.toStr()


def writeAppend(path: str, lines: List[str], encoding='UTF-8'):
    with open(path, 'a', encoding=encoding) as f:
        f.writelines(lines)


def download(url, filePath):
    r = requests.get(url)

    with open(filePath, "wb") as f:
        f.write(r.content)

