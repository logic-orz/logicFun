'''
Author: Logic
Date: 2022-05-12 14:00:34
LastEditTime: 2022-05-24 17:28:59
Description: 
'''
import os
from typing import List


from cttqFuncs.common.fileFunc import deleteFile, listDir, listFile


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
    deleteFile("./cttqFuncs.egg-info")
    clear("cttqFuncs")

