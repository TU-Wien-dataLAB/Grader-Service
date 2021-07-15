import json
from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from tornado import web


@register_handler(path=r"\/permissions\/?")
class LectureBaseHandler(ExtensionBaseHandler):
    @web.authenticated
    async def get(self):
        response = await self.request_service.request(
            "GET",
            f"{self.base_url}/permissions",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))
