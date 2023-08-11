from pyhdfs import HdfsClient


class Hdfs:
    def __init__(self, hosts: str) -> None:
        self.client = HdfsClient(hosts)

    def upload(self, fromPath: str, toPath: str):
        self.client.copy_from_local(fromPath, toPath)

    def download(self, fromPath: str, toPath: str):
        self.client.copy_to_local(fromPath, toPath)

    def listDir(self, path: str):
        return self.client.listdir(path)
