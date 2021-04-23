from jupyterhub.services.auth import HubAuthenticated
from tornado import web
from grader.common.services.request import RequestService

class GraderBaseHandler(HubAuthenticated, web.RequestHandler):
  request_service = RequestService()


