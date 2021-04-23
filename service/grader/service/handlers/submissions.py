from grader.common.registry import register_handler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from grader.common.services.request import RequestService

import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?")
class SubmissionHandler(APIHandler):
  requestservice = RequestService()
  def get(self, lecture_id: int, assignment_id: int):
    self.write(self.requestservice.request(method='GET',endpoint=self.request.path,body=''))

  def post(self, lecture_id: int, assignment_id: int):
    self.write(self.requestservice.request(method='POST',endpoint=self.request.path,body=''))




@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?")
class FeedbackHandler(APIHandler):
  requestservice = RequestService()
  def get(self, lecture_id: int, assignment_id: int):
    self.write(self.requestservice.request(method='GET',endpoint=self.request.path,body=''))

