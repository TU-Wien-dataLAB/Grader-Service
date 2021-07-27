import json
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from tornado import web
from tornado.httpclient import HTTPError


@register_handler(path=r"\/permissions\/?")
class LectureBaseHandler(ExtensionBaseHandler):
    @web.authenticated
    async def get(self):
        try:
            response = await self.request_service.request(
                "GET",
                f"{self.base_url}/permissions",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))
