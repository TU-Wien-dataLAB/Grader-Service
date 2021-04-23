from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?")
class GradingBaseHandler(ExtensionBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/auto\/?")
class GradingAutoHandler(ExtensionBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?")
class GradingManualHandler(ExtensionBaseHandler):
  pass


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?")
class GradingScoreHandler(ExtensionBaseHandler):
  pass
