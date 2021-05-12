from grader.common.models.error_message import ErrorMessage
from grader.common.registry import register_handler
from grader.service.orm.lecture import Lecture
from grader.service.orm.user import User
from grader.service.orm.takepart import Role, Scope
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from jupyter_server.utils import url_path_join
from tornado_sqlalchemy import SessionMixin
import tornado
from grader.common.models.lecture import Lecture as LectureModel
from grader.service.persistence.lectures import get_lectures

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(SessionMixin, GraderBaseHandler):
  
  @authenticated
  async def get(self):
    lectures = [role.lecture for role in self.user.roles]
    self.write(lectures)

  @authenticated
  async def post(self):
    pass # TODO: how do we define the scope when the user does not have a scope with the lecture?


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(SessionMixin, GraderBaseHandler):
  
  @authenticated
  async def put(self, lecture_id: int):
    scope = self.session.query(Role).get((self.user.name, lecture_id)).role
    if scope < Scope.instructor:
      self.write_error(403, ErrorMessage("Unauthorized!"))
      return
    body = tornado.escape.json_decode(self.request.body)
    lecture_model = LectureModel.from_dict(body)
    lecture = self.session.query(Lecture).get(lecture_id)

    lecture.name = lecture_model.name
    lecture.code = lecture_model.code
    lecture.complete = lecture_model.complete
    lecture.semester = lecture_model.semester
    
    self.session.commit()
    self.write(lecture)
  
  @authenticated
  async def get(self, lecture_id: int):
    role = self.session.query(Role).get((self.user.name, lecture_id))
    if role is None:
      self.write_error(404, ErrorMessage("Not Found!"))
      return

    self.write(role.lecture)

  @authenticated
  async def delete(self, lecture_id: int):
    pass

