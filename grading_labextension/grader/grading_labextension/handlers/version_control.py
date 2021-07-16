from grader.common.registry import register_handler
from grader.grading_labextension.handlers.base_handler import ExtensionBaseHandler
from grader.common.services.git import GitError, GitService
from tornado.web import HTTPError


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/pull\/(?P<repo>\w*)\/?"
)
class PullHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, repo: str):
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
        if repo not in {"user", "group", "source", "release"}:
            self.write_error(404)
        
        git_service = GitService(lecture_code=lecture["code"], assignment_name=assignment["name"],repo_type=repo, config=self.config)
        if not git_service.is_git():
            git_service.init()
            git_service.set_remote("grader")
        try:
            git_service.pull(force=True)
            self.write("OK")
        except GitError:
            self.write_error(400)



@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/push\/(?P<repo>\w*)\/?"
)
class PushHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int, repo: str):
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

        if repo not in {"user", "group", "source", "release"}:
            self.write_error(401)
        
        git_service = GitService(lecture_code=lecture["code"], assignment_name=assignment["name"], repo_type=repo, config=self.config)
        if not git_service.is_git():
            git_service.init()
            git_service.set_remote("grader")
        try:
            git_service.push(force=True)
            self.write("OK")
        except GitError:
            self.write_error(400)