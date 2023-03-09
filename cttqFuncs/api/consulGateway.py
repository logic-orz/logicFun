import consul
import threading
from flask import Flask
from random import choice, choices


class ConsulGateway(object):
    def __init__(self, consul_host="127.0.0.1", consul_port=8500, host="127.0.0.1"):
        """初始化,连接consul服务器"""
        self.host = host
        self._consul = consul.Consul(consul_host, consul_port)
        self.service_weight = {}

    def register_service(self, name, host, port, tags=None):
        tags = tags or []
        # 注册服务
        self._consul.agent.service.register(
            name,
            name,
            host,
            port,
            tags,
            # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
            check=consul.Check().tcp(host, port, "5s", "30s", "30s"))

    def get_service(self, name):
        _, nodes = self._consul.health.service(service=name, passing=True)
        if len(nodes) == 0:
            raise Exception('service is empty.')
        weights = []
        for node in nodes:
            service = node.get('Service')
            address = "http://{0}:{1}".format(
                service['Address'], service['Port'])
            if self.service_weight.get(address) is None:
                self.service_weight[address] = 100
            weights.append(self.service_weight[address])
        service = choices(nodes, weights=weights, k=1)[0].get("Service")
        return "http://{0}:{1}".format(service['Address'], service['Port'])

    def update_weight(self, address, success):
        if success is True:
            self.service_weight[address] = max(
                100, self.service_weight[address]+5)
        else:
            self.service_weight[address] = max(
                100, self.service_weight[address]/2)

    def app(self):
        app = Flask(__name__)

        @app.route('/health', methods=['GET'])
        def get_task():
            return '{"status":"UP"}'

        app.run(debug=False, host='0.0.0.0', port=8893)

    def health(self):
        """注册服务"""
        self.register_service("XXXXX", self.host, 8893)
        consul.Check().tcp(self.host, 8893, "5s", "30s", "30s")

        t = threading.Thread(target=self.app, name='LoopThread')
        t.start()


if __name__ == '__main__':
    c = AiopsConsul(consul_host='172.16.0.224')
    print(c.get_service("riskControl"))
