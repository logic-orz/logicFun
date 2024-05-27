import abc
import json

import requests
from requests_toolbelt import MultipartEncoder

from cttqFuncs.basic import BaseClass
from cttqFuncs.common.cacheFunc import cacheable, cachePut


class Message():
    body: str
    chat_id: str
    create_time: str
    deleted: bool
    message_id: str
    msg_type: str
    sender: dict
    update_time: str
    updated: bool


class SendMsg:
    @abc.abstractmethod
    def body():
        raise Exception("子类实现方法")


class SendMsgText(SendMsg):
    msg_type = 'text'

    def __init__(self, user_id: str, text: str) -> None:
        self.user_id = user_id
        self.text = {
            "text": text
        }

    def body(self):
        re = {
            "content": json.dumps(self.text, ensure_ascii=False),
            "receive_id": self.user_id,  # chat id
            "msg_type": SendMsgText.msg_type,
        }
        return re


class SendMsgFile(SendMsg):
    msg_type = 'file'

    def __init__(self, user_id: str, fileKey: str) -> None:
        self.user_id = user_id
        self.content = {
            "file_key": fileKey
        }

    def body(self):
        re = {
            "content": json.dumps(self.content, ensure_ascii=False),
            "receive_id": self.user_id,  # chat id
            "msg_type": SendMsgFile.msg_type,
        }
        return re


class SendMsgInteractive(SendMsg):
    msg_type = "interactive"

    def __init__(self, user_id: str, fileKey: str) -> None:
        self.user_id = user_id
        self.content = {
            "file_key": fileKey
        }

    def body(self):
        re = {
            "content": json.dumps(self.content, ensure_ascii=False),
            "receive_id": self.user_id,  # chat id
            "msg_type": SendMsgInteractive.msg_type,
        }
        return re


class TsGroupRobot():
    def __init__(self, address: str) -> None:
        self.address = address

    def sendMsg(self, msg: SendMsg):

        rsp = requests.post(
            self.address,
            headers={
                'Content-Type': 'application/json'
            },
            json=msg.body()).text
        print(rsp)
        return rsp


class TsRobot():
    tokenUrl = "https://open.feishu.cttq.com/open-apis/auth/v3/tenant_access_token/internal"
    chartMsgUrl = "https://open.feishu.cttq.com/open-apis/im/v1/messages"
    chartIdUrl = "https://open.feishu.cttq.com/open-apis/im/v1/chats"
    sendMsgUrl = "https://open.feishu.cttq.com/open-apis/im/v1/messages"
    msgParams = {"receive_id_type": "user_id"}

    def __init__(self, app_id: str, app_secret: str) -> None:
        self.app_id: str = app_id
        self.app_secret: str = app_secret

    @cacheable(ns="accessToken")
    def accessToken(self):
        headers = {
            'Content-Type': "application/json;charset=utf-8"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        rsp = requests.post(url=self.tokenUrl, headers=headers, json=data)

        return "Bearer " + rsp.json()['tenant_access_token']

    def getChatMessage(self, container_id: str):

        headers = {
            "Authorization": self.accessToken()
        }
        query = {
            "container_id_type": "chat",
            "container_id": container_id
        }

        rsp = requests.get(url=self.chartMsgUrl, headers=headers, params=query).json()
        return rsp

    def getChatId(self):

        headers = {
            "Authorization": self.accessToken()
        }
        query = {
            "user_id_type": "user_id"
        }
        rsp = requests.get(url=self.chartIdUrl, headers=headers, data=query).text
        print(rsp)

    def _upFile(self, path: str):

        url = 'https://open.feishu.cttq.com/open-apis/im/v1/files'

        query = {
            "file_type": "pdf",
            "file_name": "91282760484.pdf",
            "file": ('91282760484.pdf', open(path, 'rb'), 'text/plain')
        }

        multi_form = MultipartEncoder(query)
        headers = {
            "Authorization": self.accessToken(),
            "Content-Type": multi_form.content_type
        }
        rsp = requests.post(url, headers=headers, data=multi_form).text
        return rsp

    def sendMsg(self, msg: SendMsg):

        rsp = requests.post(
            self.sendMsgUrl,
            params=self.msgParams,
            headers={
                'Authorization': self.accessToken(),
                'Content-Type': 'application/json'
            },
            json=msg.body()).text
        print(rsp)
        return rsp


if __name__ == '__main__':
    ms = [
        ('8608858', '测试推送1'),
        ('8608858', '测试推送2')
    ]

    groupBotUrl = "https://open.feishu.cttq.com/open-apis/bot/v2/hook/bbd42f6e-d7c4-4eb5-8596-7f29562dd9fe"
    bot = TsRobot(app_id="cli_a3bcc7a2ccb8d0a7",app_secret="v0jgI4wfXzmhm4w5adnDFgz8YOPHToGc")
    bot.sendMsg(SendMsgText("8608858", "测试"))
 