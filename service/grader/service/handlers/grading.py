from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from tornado_sqlalchemy import SessionMixin
import tornado
from tornado import web


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?")
class GradingBaseHandler(GraderBaseHandler, SessionMixin):
  @authenticated
  async def get(self, lecture_id: int, assignment_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/auto\/?")
class GradingAutoHandler(GraderBaseHandler, SessionMixin):
  @authenticated
  async def post(self, lecture_id: int, assignment_id: int, user_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?")
class GradingManualHandler(GraderBaseHandler, SessionMixin):
  @authenticated
  async def post(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authenticated
  async def get(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authenticated
  async def put(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authenticated
  async def delete(self, lecture_id: int, assignment_id: int, user_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?")
class GradingScoreHandler(GraderBaseHandler):
  @authenticated
  async def get(self, lecture_id: int, assignment_id: int, user_id: int):
    pass
