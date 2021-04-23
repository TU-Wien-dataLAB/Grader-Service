from jupyter_server.base.handlers import APIHandler

class GraderHandler(APIHandler):

  @property
  def grader_authentication_header(self):
    return dict(user=self.current_user, token=self.token)