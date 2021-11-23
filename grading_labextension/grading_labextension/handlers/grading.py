from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from tornado.httpclient import HTTPError
from grading_labextension.services.git import GitService
import os

@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/auto\/?"
)
class GradingAutoHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        """Sends a GET-request to the grader service to autograde a submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        """        
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/grading/{sub_id}/auto",
                header=self.grader_authentication_header,
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
        """Generates a local git repository and pulls autograded files of a submission in the user directory

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        """        

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
            server_root_dir=self.root_dir,
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type="autograde",
            config=self.config,
        )
        git_service.path = os.path.join(
            git_service.git_root_dir,
            "manualgrade",
            git_service.lecture_code,
            git_service.assignment_name,
            sub_id,
        )
        self.log.info(f"Path: {git_service.path}")
        if not os.path.exists(git_service.path):
            os.makedirs(git_service.path, exist_ok=True)

        if not git_service.is_git():
            git_service.init()
        git_service.set_remote("autograde")
        # we just need to fetch --all and switch branch (otherwise for pull we get "fatal: refusing to merge unrelated histories")
        git_service.switch_branch(branch=f"submission_{submission['commit_hash']}")


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/feedback\/?"
)
class GenerateFeedbackHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        """Sends a GET-request to the grader service to generate feedback for a graded submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        """        

        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/grading/{sub_id}/feedback",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(response)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/pull\/feedback\/?"
)
class PullFeedbackHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        """Generates a local git repository and pulls the feedback files of a submission in the user directory 

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        """        
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
            server_root_dir=self.root_dir,
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type="feedback",
            config=self.config,
        )
        git_service.path = os.path.join(
            git_service.git_root_dir,
            "feedback",
            git_service.lecture_code,
            git_service.assignment_name,
            sub_id,
        )
        self.log.info(f"Path: {git_service.path}")
        if not os.path.exists(git_service.path):
            os.makedirs(git_service.path, exist_ok=True)

        if not git_service.is_git():
            git_service.init()
        git_service.set_remote("feedback", sub_id=sub_id)
        # we just need to fetch --all and switch branch (otherwise for pull we get "fatal: refusing to merge unrelated histories")
        git_service.switch_branch(branch=f"feedback_{submission['commit_hash']}")
        self.write("Pulled Feedback")