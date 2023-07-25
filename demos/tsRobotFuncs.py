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
    url = "https://open.feishu.cttq.com/open-apis/im/v1/messages"
    _params = {"receive_id_type": "user_id"}

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


class TsRobot():
    APP_ID: str = ""
    APP_SECRET: str = ""

    def __init__(self) -> None:
        pass

    @cacheable(ns="accessToken")
    def accessToken(self):
        headers = {
            'Content-Type': "application/json;charset=utf-8"
        }
        data = {
            "app_id": self.APP_ID,
            "app_secret": self.APP_SECRET
        }
        url = 'https://open.feishu.cttq.com/open-apis/auth/v3/tenant_access_token/internal'
        rsp = requests.post(url=url, headers=headers, json=data)
        return "Bearer " + rsp.json()['tenant_access_token']

    def getChatMessage(self):
        url = "https://open.feishu.cttq.com/open-apis/im/v1/messages"
        headers = {
            "Authorization": self.accessToken()
        }
        query = {
            "container_id_type": "chat",
            "container_id": "oc_d0cc9ebc1036960490c74a9747f26de5"
        }
        rsp = requests.get(url, headers=headers, params=query).json()

    def getChatId(self):
        url = "https://open.feishu.cttq.com/open-apis/im/v1/chats"
        headers = {
            "Authorization": self.accessToken()
        }
        query = {
            "user_id_type": "user_id"
        }
        rsp = requests.get(url, headers=headers, data=query).text

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
            SendMsg.url,
            params=SendMsg._params,
            headers={
                'Authorization': self.accessToken(),
                'Content-Type': 'application/json'
            },
            json=msg.body()).text
        print(rsp)
        return rsp


# # getMessage()
# # upFile()
# # SendMsgFile('8102784', 'file_v2_5c0eb9b7-3f69-4e81-ad50-0ee62fccd8hj')
# print(accessToken())
if __name__ == '__main__':
    ms = [
        ('8608858', '测试推送1'),
        ('8608858', '测试推送2'),
        ('17865914019', '测试推送3'),
        ('17865914019', '测试推送4')
    ]
    for userId, msg in ms:
        SendMsgText(userId, msg).send()
