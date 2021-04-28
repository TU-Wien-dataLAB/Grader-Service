from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from traitlets.config.configurable import LoggingConfigurable
from typing import Dict
from tornado.escape import json_decode

from traitlets.traitlets import Int, Unicode


class RequestService(LoggingConfigurable):
    scheme = Unicode('http', help="The http scheme to use. Either 'http' or 'https'").tag(config=True)
    host = Unicode('127.0.0.1', help="Host adress of the grader service").tag(config=True)
    port = Int(4010, help="Host port of the grader service").tag(config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.http_client = AsyncHTTPClient()

    async def request(self, method: str, endpoint: str, body: dict=None, header: Dict[str, str]=None) -> dict:
        response: HTTPResponse = await self.http_client.fetch(self.url+endpoint, method=method, headers=header, body=body)
        return json_decode(response.body)
    
    @property
    def url(self):
        return self.scheme + "://" + self.host + ":" + str(self.port)
    