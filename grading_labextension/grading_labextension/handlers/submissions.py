import json
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from grading_labextension.services.request import RequestService
from tornado.httpclient import HTTPError


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?"
)
class SubmissionHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int):
        query_params = RequestService.get_query_string(
            {
                "instructor-version": self.get_argument("instructor-version", None),
                "latest": self.get_argument("latest", None),
            }
        )
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions{query_params}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/properties\/?"
)
class SubmissionPropertiesHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, submission_id: int):
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions/{submission_id}/properties",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))

    async def put(self, lecture_id: int, assignment_id: int, submission_id: int):
        try:
            response = await self.request_service.request(
                method="PUT",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions/{submission_id}/properties",
                header=self.grader_authentication_header,
                body=self.request.body.decode("utf-8")
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?"
)
class FeedbackHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int):
        query_params = RequestService.get_query_string(
            {
                "instructor-version": self.get_argument("instructor-version", None),
                "latest": self.get_argument("latest", None),
            }
        )
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/feedback{query_params}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(response)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/(?P<feedback_id>\d*)\/?"
)
class FeedbackObjectHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, feedback_id: int):
        pass
