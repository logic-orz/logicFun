'''
Author: Logic
Date: 2022-05-23 14:33:08
LastEditTime: 2022-05-27 11:47:22
Description:
'''

from minio import Minio as MinioConnect
from minio.error import S3Error
from minio.datatypes import Object as MinioObj
from cttqFuncs.basic.configFunc import getDict
from typing import List
import cttqFuncs.basic.exFunc


class Minio():
    def __init__(self, config) -> None:
        self.client = MinioConnect(config['host'],
                                   access_key=config['user'],
                                   secret_key=config['pwd'],
                                   secure=False)
        self.bucket = config['db']

    def upload(self, remoteName, localPath, content_type="application/octet-stream", metadata: dict = {}):
        self.client.fput_object(self.bucket, remoteName, localPath,
                                content_type, metadata)

    def remove(self, name):
        self.client.remove_object(self.bucket, name)

    def download(self, name, path):
        self.client.fget_object(self.bucket, name, path)

    def listFiles(self, path: str = '') -> List[MinioObj]:
        files = list(self.client.list_objects(
            self.bucket, prefix=path,
            recursive=True,
            include_user_meta=True))

        return files

    @staticmethod
    def fixedMinio(ns='minio'):
        return Minio(getDict(ns))
