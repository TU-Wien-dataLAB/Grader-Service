from genericpath import exists
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from jupyter_server.utils import url_path_join
from tornado.httpclient import HTTPError
import json
from grading_labextension.services.git import GitError, GitService
import os


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?"
)
class GradingBaseHandler(ExtensionBaseHandler):
    pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/auto\/?"
)
class GradingAutoHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        try:
            response = await self.request_service.request(
            method="GET",
            endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/grading/{sub_id}/auto",
            header=self.grader_authentication_header
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return 
        self.write(response)



@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/manual\/?"
)
class GradingManualHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
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

            submission = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions/{sub_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type="autograde",
            config=self.config,
        )
        git_service.path = os.path.join(git_service.git_root_dir, "manualgrade", git_service.lecture_code, git_service.assignment_name,sub_id)
        self.log.info(f"Path: {git_service.path}")
        if not os.path.exists(git_service.path):
            os.makedirs(git_service.path, exist_ok=True)

        if not git_service.is_git():
          git_service.init()
          git_service.set_remote("autograde")
        git_service.pull("autograde",branch=f"submission_{submission['commit_hash']}")

@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/feedback\/?"
)
class GradingFeedbackHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
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

            submission = await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions/{sub_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type="autograde",
            config=self.config,
        )
        git_service.path = os.path.join(git_service.git_root_dir, "feedback", git_service.lecture_code, git_service.assignment_name,sub_id)
        self.log.info(f"Path: {git_service.path}")
        if not os.path.exists(git_service.path):
            os.makedirs(git_service.path, exist_ok=True)

        if not git_service.is_git():
          git_service.init()
          git_service.set_remote("feedback",sub_id)
        git_service.pull("feedback",branch=f"feedback_{submission['commit_hash']}")
        self.write("Pulled Feedback")

@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/score\/?"
)
class GradingScoreHandler(ExtensionBaseHandler):
    pass
