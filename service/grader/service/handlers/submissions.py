from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from tornado import web
from jupyter_server.utils import url_path_join

import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?")
class SubmissionHandler(GraderBaseHandler):

  @authenticated
  def get(self, lecture_id: int, assignment_id: int):
    pass

  @authenticated
  def post(self, lecture_id: int, assignment_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?")
class FeedbackHandler(GraderBaseHandler):

  @authenticated
  def get(self, lecture_id: int, assignment_id: int):
    pass

