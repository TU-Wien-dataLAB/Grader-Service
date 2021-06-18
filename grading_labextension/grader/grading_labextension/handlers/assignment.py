import json
from grader.common.services import serialize
from grader.common.registry import register_handler
from grader.common.services.git import GitService
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment
from grader.common.models.exercise import Exercise
from grader.common.models.assignment_file import AssignmentFile
from grader.common.services.request import RequestService
import tornado
import os


# TODO: Test new function
def get_assignment_with_files(lecture_name: str, assignment: Assignment) -> Assignment:
    path = os.path.join(os.path.expanduser("~"), lecture_name, assignment.name)
    os.makedirs(path, exist_ok=True)
    for file in [os.path.relpath(os.path.join(dp, f), path) for dp, dn, fn in os.walk(path) for f in fn]:
        _, ext = os.path.splitext(file)
        base_name = os.path.basename(file)
        if ext in {".ipynb", ".py"}:
            ex = Exercise()
            ex.name = base_name
            ex.a_id = assignment.id
            ex.path = file
            ex.ex_type = "nbgrader"
            ex.hashcode = None
            assignment.exercises.append(ex)
        else:
            f = AssignmentFile()
            f.name = base_name
            f.a_id = assignment.id
            f.path = file
            f.hashcode = None
            assignment.files.append(f)
    return assignment


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int):
        response = await self.request_service.request(
            method="GET",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments",
            header=self.grader_authentication_header,
        )

        lecture = await self.request_service.request(
            "GET",
            f"{self.base_url}/lectures/{lecture_id}",
            header=self.grader_authentication_header,
        )

        assignments = []
        for a in response:
            assignment = Assignment.from_dict(a)
            assignments.append(get_assignment_with_files(lecture["name"], assignment))
        self.write_json(assignments)


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

        if self.get_argument("metadata-only", "false") == "true":
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}{query_params}",
                header=self.grader_authentication_header,
            )
            self.write(json.dumps(response))
        else:
            # create git repo and push to remote
            lecture = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
            a = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
            )
            assignment = Assignment.from_dict(a)
            print("----CONFIG:", self.config)
            git_service: GitService = GitService(
                lecture["code"], assignment.name, config=self.config
            )
            git_service.init()
            git_service.set_remote(name="grader")
            git_service.pull()

            self.write_json(get_assignment_with_files(lecture["name"], assignment))

    async def delete(self, lecture_id: int, assignment_id: int):
        response = await self.request_service.request(
            method="DELETE",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
            header=self.grader_authentication_header,
        )
        self.write(json.dumps(response))
