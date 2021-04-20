from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from typing import Dict
import json


async def request(method: str, url: str, endpoint: str, body: dict, header: Dict[str, str]=None) -> dict:
    http_client = AsyncHTTPClient()
    response: HTTPResponse = await http_client.fetch(url+endpoint, method=method, headers=header, body=body)
    return json.loads(response.body)