from grader.common.registry import register_handler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from grader.common.services.request import request

@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(APIHandler):
  def get(self):
    pass    

  def post(self):
    pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(APIHandler):
  def put(self, lecture_id: int):
    pass 
  
  def get(self, lecture_id: int):
    pass
  
  def delete(self, lecture_id: int):
    pass

