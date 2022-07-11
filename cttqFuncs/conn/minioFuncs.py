'''
Author: Logic
Date: 2022-05-23 14:33:08
LastEditTime: 2022-05-27 11:47:22
FilePath: \PyShovel\impalaTableCheck\minioFuncs.py
Description: 
'''

from minio import Minio as MinioConnect
from minio.error import S3Error
from cttqFuncs.basic.configFunc import getDict


class Minio():
    def __init__(self, config) -> None:
        self.client = MinioConnect(config['host'],
                                   access_key=config['user'],
                                   secret_key=config['pwd'],
                                   secure=False)
        self.bucket = config['db']

    def upload(self, name, path, content_type="application/octet-stream"):
        self.client.fput_object(self.bucket, name, path, content_type)

    def remove(self, name):
        self.client.remove_object(self.bucket, name)

    @staticmethod
    def fixedMinio(ns='minio'):
        return Minio(getDict(ns))
