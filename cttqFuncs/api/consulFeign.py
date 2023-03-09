import requests
import logging
from consulGateway import AiopsConsul


class AiopsStarLinkFeign(object):
    def __init__(self, project='aiops-station-model'):
        """初始化，连接consul服务器"""
        self.sr = SR(project)
        self.aiops_consul = AiopsConsul(consul_host=self.sr.getProperty('default.consul_url'),
                                        consul_port='default.consul_port')
        self.client = requests.session()
        self.headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive',
                        'buc-auth-token': 'default.buc-auth-token'}

    def get(self, uri):
        try_count = 0
        while try_count < 5:
            address = self.aiops_consul.get_service('service')
            url = '{0}{1}'.format(address, uri)
            response = self.client.get(
                url=url,
                headers=self.headers)
            if response.status_code is 200:
                self.aiops_consul.update_weight(address, success=True)
                return response.content
            self.aiops_consul.update_weight(address, success=False)
            try_count += 1
            logging.warning('{0}: status_code is {1}'.format(url, response.status_code))
        raise Exception('service service is error')

    def post(self, uri, data):
        try_count = 0
        while try_count < 5:
            address = self.aiops_consul.get_service('service')
            url = '{0}{1}'.format(address, uri)
            response = self.client.post(
                url=url,
                headers=self.headers,
                data=data)
            if response.status_code is 200:
                self.aiops_consul.update_weight(address, success=True)
                return response.content
            self.aiops_consul.update_weight(address, success=False)
            try_count += 1
            logging.warning('{0}: status_code is {1}'.format(url, response.status_code))
        raise Exception('service service is error')

    def get_task(self, task_id, user):
        return self.get('/task/get/{0}?user={1}'.format(task_id, user))

    def get_and_run_task(self, task, user):
        return self.get('/task/getAndRun/{0}?user={1}'.format(task, user))


if __name__ == '__main__':
    feign = AiopsStarLinkFeign()
    print(feign.get_task('', user='sun'))
    print(feign.get_and_run_task(task="task", user='sun'))