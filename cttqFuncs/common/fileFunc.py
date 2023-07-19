import os
from ..basic.exClass import StrBuild
from ..exFunc import *
import shutil
import requests


def isExist(path):
    return os.path.exists(path)


def createFile(path):
    if not os.path.exists(path):
        open(path, 'w')


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
        return os.listdir(path).map(lambda s: path+("" if path.endswith("/") else "/")+s).filter(lambda p: os.path.isfile(p))
    return list()


def listDir(path: str):
    if os.path.exists(path):
        return os.listdir(path).map(lambda s: path+("" if path.endswith("/") else "/")+s).filter(lambda p: os.path.isdir(p))
    return list()


def listDeep(path: str):
    re = []
    files = listFile(path)
    for f in files:
        re.append(f)
    dirs = listDir(path)
    for d in dirs:
        re.extend(listFileDeep(d))
    return re


def readLines(path: str, limit: int = -1, encoding='UTF-8'):
    re: List[str] = list()
    if os.path.exists(path):
        for line in open(path, 'r', encoding=encoding):
            if line.endswith("\n"):
                line = line[:-1]
            re.append(line)

            if limit > 0 and len(re) >= limit:
                break

        if len(re) > 0 and re[-1] == '':
            re = re[:-1]
    return re


def readStr(path: str, encoding='UTF-8') -> str:

    sb = StrBuild()
    if os.path.exists(path):
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
