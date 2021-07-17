import json
import logging
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
import tornado
from tornado import web
from grading_labextension.services.request import RequestService


@register_handler(path=r"\/lectures\/?")
class LectureBaseHandler(ExtensionBaseHandler):
    @web.authenticated
    async def get(self):
        logging.getLogger().critical("GET LECTURES")
        query_params = RequestService.get_query_string(
            {"semester": self.get_argument("semester", None)}
        )
        response = await self.request_service.request(
            "GET",
            f"{self.base_url}/lectures{query_params}",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))

    @web.authenticated
    async def post(self):
        response = await self.request_service.request(
            "POST",
            f"{self.base_url}/lectures",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/?")
class LectureObjectHandler(ExtensionBaseHandler):
    @web.authenticated
    async def put(self, lecture_id: int):
        data = tornado.escape.json_decode(self.request.body)
        response_data: dict = await self.request_service.request(
            "PUT",
            f"{self.base_url}/lectures/{lecture_id}",
            body=data,
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response_data))

    @web.authenticated
    async def get(self, lecture_id: int):
        response_data: dict = await self.request_service.request(
            "GET",
            f"{self.base_url}/lectures/{lecture_id}",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response_data))

    @web.authenticated
    async def delete(self, lecture_id: int):
        await self.request_service.request(
            "DELETE",
            f"{self.base_url}/lectures/{lecture_id}",
            header=self.grader_authentication_header,
        )
        self.write("OK")
