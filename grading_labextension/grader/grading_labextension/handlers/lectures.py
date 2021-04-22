from grader.common.registry import register_handler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from tornado import web
from grader.common.services.request import RequestService

service = RequestService()

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(APIHandler):
  @web.authenticated
  async def get(self):
    self.write(await service.request("GET", "/lectures"))

  @web.authenticated
  async def post(self):
    self.write(await service.request("POST", "/lectures"))


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(APIHandler):
  
  @web.authenticated
  async def put(self, lecture_id: int):
    data = tornado.escape.json_decode(self.request.body)
    response_data: dict = await service.request("PUT", f"/lectures/{lecture_id}", body=data)
    self.write(response_data)
  
  @web.authenticated
  async def get(self, lecture_id: int):
    response_data: dict = await service.request("GET", f"/lectures/{lecture_id}")
    self.write(response_data)
  
  @web.authenticated
  async def delete(self, lecture_id: int):
    await service.request("DELETE", f"/lectures/{lecture_id}")
    self.write("OK")

