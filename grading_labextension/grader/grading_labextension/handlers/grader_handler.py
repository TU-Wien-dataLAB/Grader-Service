from grader.common.services.request import RequestService
from jupyter_server.base.handlers import APIHandler

class GraderHandler(APIHandler):
  request_service = RequestService()

  @property
  def grader_authentication_header(self):
    return dict(user=self.current_user, token=self.token)