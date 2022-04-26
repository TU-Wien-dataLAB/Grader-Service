from grading_labextension.services.request import RequestService
from jupyter_server.base.handlers import APIHandler
import os
from tornado.httpclient import HTTPClient, HTTPClientError
from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Unicode

# test_token: ebce9dfa2a694fb9bb06883bd8bb6012

class HandlerConfig(SingletonConfigurable):
    hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL"), help="The url of the hubs api.").tag(config=True)
    hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN"), help="The authorization token to access the hub api").tag(config=True)
    hub_user = Unicode(os.environ.get("JUPYTERHUB_USER"), help="The user name in jupyter hub.").tag(config=True)


class ExtensionBaseHandler(APIHandler):
    """
    BaseHandler for all server-extension handler
    """
    request_service = RequestService()
    http_client = HTTPClient()
    base_url = "/services/grader"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.root_dir = os.path.expanduser(self.settings["server_root_dir"])

    @property
    def grader_authentication_header(self):
        """Returns the authentication header

        :return: authentication header
        :rtype: dict
        """

        return dict(Authorization="Token " + HandlerConfig.instance().hub_api_token)

    async def get_lecture(self, lecture_id):
        try:
            lecture = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
            return lecture
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

    async def get_assignment(self, lecture_id, assignment_id):
        try:
            assignment = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
            )
            return assignment
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
