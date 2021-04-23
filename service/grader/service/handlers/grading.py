from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
from tornado import web


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?")
class GradingBaseHandler(GraderBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/auto\/?")
class GradingAutoHandler(GraderBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?")
class GradingManualHandler(GraderBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?")
class GradingScoreHandler(GraderBaseHandler):
  pass
