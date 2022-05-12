import os

from myFunc.basic.fileFunc import deleteFile, listDir,listFile


def clear(filepath):        
    dirs = listDir(filepath)
    for dir in dirs:
        if dir.endswith("/__pycache__"):
            deleteFile(dir)
        else:
            clear(dir)


if __name__ == "__main__":
    deleteFile("./build")
    deleteFile("./dist")
    deleteFile("./myFunc.egg-info")

    clear("myFunc")

