from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment
from grader.common.services.request import RequestService
import tornado

@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(ExtensionBaseHandler):
  def get(self, lecture_id: int):
    self.write(self.request_service.request(method='GET',endpoint=self.request.path,body=''))


  def post(self, lecture_id: int):
    self.write(self.request_service.request(method='POST',endpoint=self.request.path,body=''))


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?")
class AssignmentObjectHandler(ExtensionBaseHandler):
  def put(self, lecture_id: int, assignment_id: int):
    pass 
  
  def get(self, lecture_id: int, assignment_id: int):
    self.write(self.request_service.request(method='GET',endpoint=self.request.path,body=''))

  
  def delete(self, lecture_id: int, assignment_id: int):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/file\/(?P<file_id>\d*)\/?")
class AssignmentDataHandler(ExtensionBaseHandler):
  def get(self, lecture_id: int, assignment_id: int, file_id: int):
    pass