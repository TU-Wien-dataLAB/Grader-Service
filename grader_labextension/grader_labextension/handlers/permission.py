import json
from grader_labextension.registry import register_handler
from grader_labextension.handlers.base_handler import ExtensionBaseHandler
from tornado import web
from tornado.httpclient import HTTPError


@register_handler(path=r"\/permissions\/?")
class PermissionBaseHandler(ExtensionBaseHandler):
    @web.authenticated
    async def get(self):
        """ Sends a GET-request to the grader service and returns the permissions of a user
        """
        try:
            response = await self.request_service.request(
                "GET",
                f"{self.service_base_url}/permissions",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))
