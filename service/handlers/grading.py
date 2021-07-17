from registry import register_handler
from handlers.base_handler import GraderBaseHandler, authorize
from jupyter_server.utils import url_path_join
from orm.takepart import Scope


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?")
class GradingBaseHandler(GraderBaseHandler):
  @authorize([Scope.student, Scope.tutor, Scope.instructor])
  async def get(self, lecture_id: int, assignment_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/auto\/?")
class GradingAutoHandler(GraderBaseHandler):
  @authorize([Scope.tutor, Scope.instructor])
  async def post(self, lecture_id: int, assignment_id: int, user_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?")
class GradingManualHandler(GraderBaseHandler):
  @authorize([Scope.tutor, Scope.instructor])
  async def post(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authorize([Scope.tutor, Scope.instructor])
  async def get(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authorize([Scope.tutor, Scope.instructor])
  async def put(self, lecture_id: int, assignment_id: int, user_id: int):
    pass

  @authorize([Scope.instructor])
  async def delete(self, lecture_id: int, assignment_id: int, user_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?")
class GradingScoreHandler(GraderBaseHandler):
  @authorize([Scope.student, Scope.tutor, Scope.instructor])
  async def get(self, lecture_id: int, assignment_id: int, user_id: int):
    pass
