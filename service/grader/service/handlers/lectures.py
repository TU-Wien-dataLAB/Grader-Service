from grader.common.registry import register_handler
from grader.common.models.user import User
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from jupyter_server.utils import url_path_join
import tornado
from tornado import web
from tornado_sqlalchemy import SessionMixin
from grader.service.persistence.lectures import get_lectures

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(GraderBaseHandler, SessionMixin):
  
  @authenticated
  async def get(self):
    self.write(self.current_user.lectures)
    # self.write(get_lectures(self.current_user))

  @authenticated
  async def post(self):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(GraderBaseHandler, SessionMixin):
  
  @authenticated
  async def put(self, lecture_id: int):
    pass
  
  @authenticated
  async def get(self, lecture_id: int):
    pass
  
  @authenticated
  async def delete(self, lecture_id: int):
    pass

