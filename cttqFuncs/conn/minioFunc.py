from typing import List

from minio import Minio as MinioConnect
from minio.datatypes import Object as MinioObj
from minio.error import S3Error

from ..basic.configFunc import getDict
from ..exFunc import *


class Minio():
    def __init__(self, config) -> None:
        self.client = MinioConnect(config['host'],
                                   access_key=config['user'],
                                   secret_key=config['pwd'],
                                   secure=False)
        self.bucket = config['db']

    def upload(self, remoteName, localPath: str = None, fileData=None, bucket: str = None, content_type="application/octet-stream", metadata: dict = {}):
        if not bucket:
            bucket = self.bucket

        if fileData:
            self.client.put_object(bucket_name=bucket, object_name=remoteName, data=fileData, content_type=content_type, metadata=metadata)
        else:
            self.client.fput_object(bucket_name=bucket, object_name=remoteName, file_path=localPath, content_type=content_type, metadata=metadata)

    def remove(self, name):
        self.client.remove_object(self.bucket, name)

    def download(self, name, bucket: str = None, path: str = None):
        if not bucket:
            bucket = self.bucket
        if path:
            self.client.fget_object(bucket_name=bucket, object_name=name, file_path=path)
            return None
        else:
            data = self.client.get_object(bucket_name=bucket, object_name=name)
            return data

    def listFiles(self, bucket: str = None, path: str = '') -> List[MinioObj]:
        if not bucket:
            bucket = self.bucket

        files = list(self.client.list_objects(
            bucket, prefix=path,
            recursive=True,
            include_user_meta=True))

        return files

    @staticmethod
    def fix(ns='minio'):
        return Minio(getDict(ns))
