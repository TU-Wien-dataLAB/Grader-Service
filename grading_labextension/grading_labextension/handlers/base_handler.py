import logging
from grading_labextension.services.request import RequestService
from jupyter_server.base.handlers import APIHandler
from jupyterhub.services.auth import HubAuthenticated
import os
from tornado import web
from tornado import httpclient
from tornado.httpclient import HTTPClient
from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Unicode

# test_token: ebce9dfa2a694fb9bb06883bd8bb6012

class HandlerConfig(SingletonConfigurable):
  hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL"), help="The url of the hubs api.").tag(config=True)
  hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN"), help="The authorization token to access the hub api").tag(config=True)
  hub_user = Unicode(os.environ.get("JUPYTERHUB_USER"), help="The user name in jupyter hub.").tag(config=True)


class ExtensionBaseHandler(APIHandler):
  request_service = RequestService()
  http_client = HTTPClient()
  base_url = "/services/grader"

  # curl -X GET -H "Authorization: token ebce9dfa2a694fb9bb06883bd8bb6012" "http://128.130.202.214:8080/hub/api/authorizations/token/ebce9dfa2a694fb9bb06883bd8bb6012"
  @property
  def grader_authentication_header(self):
    logging.getLogger().critical(HandlerConfig.instance().hub_api_token)
    return dict(Authorization="Token " + HandlerConfig.instance().hub_api_token)
