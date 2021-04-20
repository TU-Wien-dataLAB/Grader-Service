from tornado.httpclient import AsyncHTTPClient


async def request(method, url, endpoint, body, header=None):
    http_client = AsyncHTTPClient()
    response = await http_client.fetch(url+endpoint, method=method, headers=header, body=body)
    return dict(response.body)