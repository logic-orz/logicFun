from demos.rpcFunc import runRpcServer, loadRpcClient, BasicRpc
import zerorpc
import time
client = loadRpcClient()
while True:
    time.sleep(2)
    print(client.test())
