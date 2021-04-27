from jupyterhub.services.auth import HubAuthenticated
from tornado import web
from tornado import httputil
from typing import Any
from grader.common.services.request import RequestService
from grader.service.main import GraderApp
from urllib.parse import ParseResult, urlparse
import functools
from typing import Awaitable, Callable, Optional
from tornado.web import HTTPError, RequestHandler

class GraderBaseHandler(web.RequestHandler):
  request_service = RequestService()
  hub_request_service = RequestService()

  def __init__(self, application: GraderApp, request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
      super().__init__(application, request, **kwargs)
      
      self.application: GraderApp = self.application  # add type hint for application
      hub_api_parsed: ParseResult = urlparse(self.application.hub_api_url)
      self.hub_request_service.scheme = hub_api_parsed.scheme
      self.hub_request_service.host, self.hub_request_service.port = httputil.split_host_and_port(hub_api_parsed.netloc)
      self.hub_api_base_path: str = hub_api_parsed.path

  def get_current_user(self):
      token = None
      for (k,v) in sorted(self.request.headers.get_all()):
        if k == "Authorization":
          token = v.replace("token ", "")
      if not token: # request has to have an Authorization token for JupyterHub
        return None
      
      try:
        print(self.application.hub_api_token)
        user: dict = self.hub_request_service.request_sync("GET", self.hub_api_base_path + f"/authorizations/token/{token}", header={"Authorization": f"token {self.application.hub_api_token}"})
        print("User:", user)
      except Exception:
        return None
      return user

def authenticated(
    method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Optional[Awaitable[None]]]:
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, an `tornado.web.HTTPError` with cod 403 will be raised.
    """

    @functools.wraps(method)
    def wrapper(  # type: ignore
        self: GraderBaseHandler, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper