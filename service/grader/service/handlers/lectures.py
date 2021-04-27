from grader.common.registry import register_handler
from service.handlers.base_handler import GraderBaseHandler
from jupyter_server.utils import url_path_join
import tornado
from tornado import web
from grader.common.services.request import RequestService
from tornado_sqlalchemy import SessionMixin
from sqlalchemy import create_engine
from service.persistence.database import get_all

service = RequestService()
engine = create_engine('sqlite:///grader.db', echo=True)

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(SessionMixin, GraderBaseHandler):
  
  @web.authenticated
  async def get(self):
    get_all('lectures')

  @web.authenticated
  async def post(self):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(SessionMixin, GraderBaseHandler):
  
  @web.authenticated
  async def put(self, lecture_id: int):
    pass
  
  @web.authenticated
  async def get(self, lecture_id: int):
    pass
  
  @web.authenticated
  async def delete(self, lecture_id: int):
    pass

