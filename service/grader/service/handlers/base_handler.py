import functools
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import ParseResult, urlparse
import logging
from grader.common.services.request import RequestService
from grader.service.main import GraderService
from jupyterhub.services.auth import HubAuthenticated
from tornado import httputil, web
from tornado.web import HTTPError, RequestHandler


class GraderBaseHandler(web.RequestHandler):
  request_service = RequestService()
  hub_request_service = RequestService()

  def __init__(self, application: GraderService, request: httputil.HTTPServerRequest, **kwargs: Any) -> None:
      super().__init__(application, request, **kwargs)
      
      self.application: GraderService = self.application  # add type hint for application
      hub_api_parsed: ParseResult = urlparse(self.application.hub_api_url)
      self.hub_request_service.scheme = hub_api_parsed.scheme
      self.hub_request_service.host, self.hub_request_service.port = httputil.split_host_and_port(hub_api_parsed.netloc)
      self.hub_api_base_path: str = hub_api_parsed.path
  
  async def prepare(self) -> Optional[Awaitable[None]]:
    """
    This is a workaround for async authentication. `get_current_user` cannot be asyncronous and a request cannot be made in a blocking manner.
    This sets the `current_user` property before each request before being checked by the `authenticated` decorator.
    """
    user = await self.get_current_user_async()
    self.current_user = user

  async def get_current_user_async(self):
      token = None
      for (k,v) in sorted(self.request.headers.get_all()):
        if k == "Authorization":
          token = v.replace("token ", "")
      if not token: # request has to have an Authorization token for JupyterHub
        return None
      
      try:
        user: dict = await self.hub_request_service.request("GET", self.hub_api_base_path + f"/authorizations/token/{token}", header={"Authorization": f"token {self.application.hub_api_token}"})
      except Exception as e:
        logging.getLogger().error(e)
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
