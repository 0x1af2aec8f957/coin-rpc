import base64
import decimal
from log.config import LOG
import json
from request import config as conf

try:
    import http.client as httplib
except ImportError:
    import httplib

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

USER_AGENT = "BTM/COIN"


class Proxy:
    def __init__(self, url=conf.URL, timeout=30):
        self.url = urlparse.urlparse(url)
        self.timeout = timeout
        port = self.url.port or 80  # 节点端口

        (user, passwd) = (self.url.username, self.url.password)  # 提取用户名和密码
        try:
            user = user.encode('utf8')
        except AttributeError:
            pass
        try:
            passwd = passwd.encode('utf8')
        except AttributeError:
            pass
        self.__auth_header = b'Basic ' + base64.b64encode(user + b':' + passwd)  # 头认证[而非链接携带用户名和密码]
        self.__conn = eval(
            f'httplib.{self.url.scheme.upper()}Connection(self.url.hostname, port, timeout = timeout)')  # 请求对象

    # @classmethod
    def get_response(self, path='', data=None):
        '''

        :param path: str 请求路径,如果是json-rpc可省略
        :param data: json-rpc or json
        :return: json or json-rpc[节点数据]
        '''
        self.__conn.request('POST',
                            self.url.path + path,
                            json.dumps(data) if data else None,
                            {'Host': self.url.hostname,
                             'User-Agent': USER_AGENT,
                             'Authorization': self.__auth_header,
                             'Content-type': 'application/json'})  # 请求体
        # self.__conn.sock.settimeout(self.timeout)  # 设置超时
        http_response = self.__conn.getresponse()  # 获取节点返回的参数
        response = http_response.read().decode('utf8')  # 解码参数
        # LOG.info(f'POST {path} {response}')
        return json.loads(response)  # 节点返回的数据[可以是非jsonRpc]

    def run(self, param, callback=None):
        '''

        :param param:function [返回一个get_response需要的参数]
        :param callback:function
        :return: json[节点数据] 或 function[callback自定义返回数据[这里可以根据不同的币种处理数据库字段]]
        '''
        return callback(self.get_response(param())) if callback else self.get_response(param())


send = Proxy(conf.URL)
send.get_response('/get-block', {"block_height": 1})
