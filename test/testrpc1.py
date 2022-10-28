from demos.rpcFunc import runRpcServer, loadRpcClient, BasicRpc
import zerorpc
import asyncio


class TmpA(BasicRpc):
    i=0
    def test(self):
        self.i+=1
        print(self.i)
        return 'test'

    @zerorpc.stream
    def gen(self, start, end):
        for i in range(start, end):
            yield i


runRpcServer(TmpA())
