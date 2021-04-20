from grader.common.registry import register_handler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?")
class SubmissionHandler(APIHandler):
  def get(self, lecture_id: int, assignment_id: int):
    pass

  def post(self, lecture_id: int, assignment_id: int):
    pass



@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?")
class FeedbackHandler(APIHandler):
  def get(self, lecture_id: int, assignment_id: int):
    pass
