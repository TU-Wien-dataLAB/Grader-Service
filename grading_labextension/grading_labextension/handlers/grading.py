from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from tornado.httpclient import HTTPError
import json




@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?")
class GradingBaseHandler(ExtensionBaseHandler):
  pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/auto\/?")
class GradingAutoHandler(ExtensionBaseHandler):
  async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
    try:
      response = await self.request_service.request(
      method="GET",
      endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/grading/{sub_id}/auto",
      header=self.grader_authentication_header
      )
    except HTTPError as e:
      self.set_status(e.code)
      self.write_error(e.code)
      return 
    self.write(response)


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?")
class GradingManualHandler(ExtensionBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?")
class GradingScoreHandler(ExtensionBaseHandler):
  pass 
