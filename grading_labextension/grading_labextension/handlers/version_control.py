import json
import sys
import os
from grading_labextension.registry import register_handler
from grading_labextension.handlers.base_handler import ExtensionBaseHandler
from grading_labextension.services.git import GitError, GitService
from tornado.httpclient import HTTPError, HTTPResponse
from grader_convert.converters.generate_assignment import GenerateAssignment


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/generate\/?"
)
class GenerateHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int):
        """ Generates the release files from the source files of a assignment

        Args:
            lecture_id (int): id of the lecture
            assignment_id (int): id of the assignment
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
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        code = lecture["code"]
        name = assignment["name"]

        generator = GenerateAssignment(
            input_dir=f"~/source/{code}/{name}",
            output_dir=f"~/release/{code}/{name}",
            file_pattern="*.ipynb",
        )
        generator.force = True
        self.log.info("Starting GenerateAssignment converter")
        try:
            generator.start()
        except:
            e = sys.exc_info()[0]
            self.log.error(e)
            self.set_status(400)
            self.write_error("Could not generate assignment")
        try:
            gradebook_path = os.path.join(generator._output_directory, "gradebook.json")
            os.remove(gradebook_path)
            self.log.info(f"Successfully deleted {gradebook_path}")
        except OSError as e:
            self.log.error(f"Could delete {gradebook_path}! Error: {e.strerror}")
        self.log.info("GenerateAssignment conversion done")
        self.write({"cool": "cool"})


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/pull\/(?P<repo>\w*)\/?"
)
class PullHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, repo: str):
        """ Creates a local repository and pulls the specified repo type

        Args:
            lecture_id (int): id of the lecture
            assignment_id (int): id of the assignment
            repo (str): type of the repository
        """
        if repo not in {"assignment", "source", "release"}:
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
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
            force_user_repo=True if repo == "release" else False,
        )
        try:
            if not git_service.is_git():
                git_service.init()
                git_service.set_author()
            git_service.set_remote(f"grader_{repo}")
            try:
                git_service.pull(f"grader_{repo}", force=True)
            except GitError as e:
                self.log.error("GitError:\n" + e.error)
            self.write("OK")
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
            self.write_error(400)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/push\/(?P<repo>\w*)\/?"
)
class PushHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int, repo: str):
        """ Pushes from the local repositories to remote
            If the repo type is release, it also generate the release files and updates the assignmentproperties in the grader service

        Args:
            lecture_id (int): id of the lecture
            assignment_id (int): id of the assignment
            repo (str): type of the repository
        """
        if repo not in {"assignment", "source", "release"}:
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
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
        )

        if repo == "release":
            git_service.delete_repo_contents(include_git=True)
            src_path = GitService(
                lecture["code"],
                assignment["name"],
                repo_type="source",
                config=self.config,
            ).path
            git_service.copy_repo_contents(src=src_path)

            # call nbconvert before pushing
            generator = GenerateAssignment(
                input_dir=src_path, output_dir=git_service.path, file_pattern="*.ipynb"
            )
            generator.force = True
            self.log.info("Starting GenerateAssignment converter")
            generator.start()
            self.log.info("GenerateAssignment conversion done")

            try:
                gradebook_path = os.path.join(git_service.path, "gradebook.json")
                with open(gradebook_path, "r") as f:
                    gradebook_json: dict = json.load(f)
            except FileNotFoundError:
                return

            self.log.info(f"Setting properties of assignment from {gradebook_path}")
            response: HTTPResponse = await self.request_service.request(
                "PUT",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/properties",
                header=self.grader_authentication_header,
                body=gradebook_json,
                decode_response=False,
            )
            if response.code == 200:
                self.log.info("Properties set for assignment")
            else:
                self.log.error(
                    f"Could not set assignment properties! Error code {response.code}"
                )

            try:
                os.remove(gradebook_path)
                self.log.info(f"Successfully deleted {gradebook_path}")
            except OSError as e:
                self.log.error(
                    f"Cannot delete {gradebook_path}! Error: {e.strerror}\nAborting push!"
                )
                return

        self.log.info(f"File contents of {repo}: {git_service.path}")
        self.log.info(",".join(os.listdir(git_service.path)))

        try:
            if not git_service.is_git():
                git_service.init()
                git_service.set_author()
                # TODO: create .gitignore file
            git_service.set_remote(f"grader_{repo}")
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
            self.write_error(400)
            return

        try:
            git_service.commit()
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
        ## committing might fail because there is nothing to commit -> try to push regardless
        try:
            git_service.push(f"grader_{repo}", force=True)
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
            self.write_error(400)
            return
        self.write("OK")
