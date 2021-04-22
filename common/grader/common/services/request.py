from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from traitlets.config.configurable import Configurable
from typing import Dict
import json

from traitlets.traitlets import Int, Unicode


class RequestService(Configurable):
    host = Unicode('127.0.0.1', help="Host adress of the grader service").tag(config=True)
    port = Int(8888, help="Host port of the grader service").tag(config=True)

    async def request(self,method: str, endpoint: str, body: dict, header: Dict[str, str]=None) -> dict:
        http_client = AsyncHTTPClient()
        response: HTTPResponse = await http_client.fetch(self.url+endpoint, method=method, headers=header, body=body)
        return json.loads(response.body)
    
    @property
    def url(self):
        return self.host + str(self.port)