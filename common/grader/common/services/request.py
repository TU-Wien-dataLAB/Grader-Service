from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from traitlets.config.configurable import Configurable
from traitlets import Unicode
from typing import Dict
import json


class RequestService(Configurable):
    url = Unicode('127.0.0.1', help="Adress to backend or grader").tag(config=True)

    async def request(self,method: str, endpoint: str, body: dict, header: Dict[str, str]=None) -> dict:
        http_client = AsyncHTTPClient()
        response: HTTPResponse = await http_client.fetch(self.url+endpoint, method=method, headers=header, body=body)
        return json.loads(response.body)