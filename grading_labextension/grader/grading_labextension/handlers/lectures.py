from grader.common.registry import register_handler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from grader.common.services.request import RequestService

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(APIHandler):
  requestservice = RequestService()
  def get(self):
    self.write(self.requestservice.request(method='GET',endpoint=self.request.path,body=''))

  def post(self, lecture_id: int):
    self.write(self.requestservice.request(method='POST',endpoint=self.request.path,body=lecture_id))



@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(APIHandler):
  requestservice = RequestService()
  def put(self, lecture_id: int):
    pass 
  
  def get(self, lecture_id: int):
    self.write(self.requestservice.request(method='GET',endpoint=self.request.path+'/'+lecture_id,body=''))

  
  def delete(self, lecture_id: int):
    pass

