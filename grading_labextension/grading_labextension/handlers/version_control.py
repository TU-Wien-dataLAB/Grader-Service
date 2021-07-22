import logging
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from grading_labextension.services.git import GitError, GitService
from tornado.httpclient import HTTPError


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/pull\/(?P<repo>\w*)\/?"
)
class PullHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, repo: str):
        if repo not in {"user", "group", "source", "release"}:
            self.write_error(404)
        try:
            lecture = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
            assignment = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
        )
        try:
            if not git_service.is_git():
                git_service.init()
                git_service.set_remote("grader")
            git_service.pull("grader", force=True)
            self.write("OK")
        except GitError:
            self.write_error(400)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/push\/(?P<repo>\w*)\/?"
)
class PushHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int, repo: str):
        if repo not in {"user", "group", "source", "release"}:
            self.write_error(401)
        try:
            lecture = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
            assignment = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
        )
        try:
            if not git_service.is_git():
                git_service.init()
                git_service.set_remote("grader")
            git_service.push("grader", force=True)
            self.write("OK")
        except GitError:
            self.write_error(400)