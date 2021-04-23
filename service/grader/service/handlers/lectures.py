from grader.common.registry import register_handler
from jupyter_server.utils import url_path_join
import tornado
from tornado import web
from grader.common.services.request import RequestService
from tornado_sqlalchemy import SessionMixin

service = RequestService()

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(SessionMixin, web.RequestHandler):
  
  @web.authenticated
  async def get(self):
    pass

  @web.authenticated
  async def post(self):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(SessionMixin, web.RequestHandler):
  
  @web.authenticated
  async def put(self, lecture_id: int):
    pass
  
  @web.authenticated
  async def get(self, lecture_id: int):
    pass
  
  @web.authenticated
  async def delete(self, lecture_id: int):
    pass

