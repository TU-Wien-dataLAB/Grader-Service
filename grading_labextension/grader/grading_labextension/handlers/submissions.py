import json
from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from grader.common.services.request import RequestService

import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?")
class SubmissionHandler(ExtensionBaseHandler):
  async def get(self, lecture_id: int, assignment_id: int):
    response = await self.request_service.request(method='GET',endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions", header=self.grader_authentication_header)
    self.write(json.dumps(response))

  async def post(self, lecture_id: int, assignment_id: int):
    data = tornado.escape.json_decode(self.request.body)
    response = await self.request_service.request(method='POST',endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions", body=data, header=self.grader_authentication_header)
    self.write(json.dumps(response))




@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?")
class FeedbackHandler(ExtensionBaseHandler):
  async def get(self, lecture_id: int, assignment_id: int):
    response = await self.request_service.request(method='GET',endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/feedback", header=self.grader_authentication_header)
    self.write(json.dumps(response))
