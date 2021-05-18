import json
from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment
from grader.common.services.request import RequestService
import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int):
        response = await self.request_service.request(
            method="GET",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))

    async def post(self, lecture_id: int):
        data = tornado.escape.json_decode(self.request.body)
        response = await self.request_service.request(
            method="POST",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments",
            body=data,
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int):
        data = tornado.escape.json_decode(self.request.body)
        response = await self.request_service.request(
            method="PUT",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
            body=data,
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))

    async def get(self, lecture_id: int, assignment_id: int):
        query_params = RequestService.get_query_string(
            {
                "instructor-version": self.get_argument("instructor-version", None),
                "metadata-only": self.get_argument("metadata-only", None),
            }
        )
        response = await self.request_service.request(
            method="GET",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}{query_params}",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))

    async def delete(self, lecture_id: int, assignment_id: int):
        response = await self.request_service.request(
            method="DELETE",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/file\/(?P<file_id>\d*)\/?"
)
class AssignmentDataHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, file_id: int):
        pass  # TODO: implement
