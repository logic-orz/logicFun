import zipfile


class ZipFile():
    def __init__(self, path: str, isAppend: bool = False, overWrite: bool = False) -> None:
        if isAppend:
            self.f = zipfile.ZipFile(path, 'a')
        elif overWrite:
            self.f = zipfile.ZipFile(path, 'w')
        else:
            self.f = zipfile.ZipFile(path)

    @property
    def names(self):
        return self.f.namelist()

    def extractAll(self, path):
        self.f.extractall(path)

    def extractOne(self, name, path):
        self.f.extract(name, path)
