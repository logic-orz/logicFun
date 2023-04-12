import zipfile


class ZipFile():
    def __init__(self, path: str, isAppend: bool = False, overWrite: bool = False) -> None:
        if isAppend:
            self.f = zipfile.ZipFile(path, 'a')
        elif overWrite:
            self.f = zipfile.ZipFile(path, 'w')
        else:
            self.f = zipfile.ZipFile(path,'r')

    @property
    def names(self):
        return self.f.namelist()

    def extractAll(self, path):
        self.f.extractall(path)

    def extractOne(self, name, path):
        self.f.extract(name, path)
    
    def addFile(self,name,path):
        self.f.write(path,name)
        
        
    def close(self):
        self.f.close()


if __name__ =='__main__':
    zf=ZipFile('./test.zip',isAppend=True)
    
    # zf.addFile('test1.py','./test/testrpc1.py')
    print(zf.names)
    
    zf.close()