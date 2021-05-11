from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from grader.service.persistence.submissions import *
from tornado import web
from jupyter_server.utils import url_path_join
from tornado_sqlalchemy import SessionMixin

import tornado
import json


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?")
class SubmissionHandler(GraderBaseHandler, SessionMixin):

  @authenticated
  def get(self, lecture_id: int, assignment_id: int):
    response = json.dumps({"user": self.current_user, "submissions": get_submissions(self.current_user, assignment_id, True)})
    self.write(response)

  @authenticated
  def post(self, lecture_id: int, assignment_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?")
class FeedbackHandler(GraderBaseHandler, SessionMixin):

  @authenticated
  def get(self, lecture_id: int, assignment_id: int):
    pass

