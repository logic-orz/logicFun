'''
Author: Logic
Date: 2022-05-12 14:00:34
LastEditTime: 2022-05-24 17:28:59
Description: 
'''
import os
from typing import List
import shutil

import cttqFuncs


def deleteFile(path: str):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            try:
                shutil.rmtree(path)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))


def listDir(path: str):
    if os.path.exists(path):
        return os.listdir(path).map(lambda s: path + ("" if path.endswith("/") else "/") + s).filter(lambda p: os.path.isdir(p))
    return list()


def clear(filepath):
    dirs: List[str] = listDir(filepath)
    for dir in dirs:
        if dir.endswith("/__pycache__"):
            deleteFile(dir)
        else:
            clear(dir)


if __name__ == "__main__":
    deleteFile("./build")
    deleteFile("./dist")
    deleteFile("./logicFun.egg-info")
    clear("logicFun")

