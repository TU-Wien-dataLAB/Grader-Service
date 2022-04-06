import json
import os
import sys
from urllib.parse import unquote, quote

from jsonschema.exceptions import ValidationError
from tornado.web import HTTPError

from grader_convert.converters.base import GraderConvertException
from grader_convert.converters.generate_assignment import GenerateAssignment
from .base_handler import ExtensionBaseHandler
from ..api.models.submission import Submission
from ..registry import register_handler
from ..services.git import GitError, GitService
from tornado.httpclient import HTTPClientError, HTTPResponse


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/generate\/?"
)
class GenerateHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int):
        """Generates the release files from the source files of a assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
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
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        code = lecture["code"]
        name = assignment["name"]

        generator = GenerateAssignment(
            input_dir=f"{self.root_dir}/source/{code}/{name}",
            output_dir=f"{self.root_dir}/release/{code}/{name}",
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
            self.write_error(400)
            return
        try:
            gradebook_path = os.path.join(generator._output_directory, "gradebook.json")
            os.remove(gradebook_path)
            self.log.info(f"Successfully deleted {gradebook_path}")
        except OSError as e:
            self.log.error(f"Could delete {gradebook_path}! Error: {e.strerror}")
        self.log.info("GenerateAssignment conversion done")
        self.write("OK")


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/log\/(?P<repo>\w*)\/?"
)
class GitLogHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, repo: str):
        if repo not in {"assignment", "source", "release"}:
            self.write_error(404)
        n_history = int(self.get_argument("n", "10"))
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
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            server_root_dir=self.root_dir,
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
            force_user_repo=True if repo == "release" else False,
        )
        git_service.set_remote(f"grader_{repo}")
        git_service.fetch_all()
        logs = git_service.get_log(n_history)
        self.write(json.dumps(logs))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/pull\/(?P<repo>\w*)\/?"
)
class PullHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, repo: str):
        """Creates a local repository and pulls the specified repo type

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param repo: type of the repository
        :type repo: str
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
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            server_root_dir=self.root_dir,
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
        """Pushes from the local repositories to remote
            If the repo type is release, it also generate the release files and updates the assignment properties in the grader service

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param repo: type of the repository
        :type repo: str
        """
        if repo not in {"assignment", "source", "release"}:
            self.write_error(404)
        commit_message = self.get_argument("commit-message", None)
        submit = self.get_argument("submit", "false") == "true"
        if repo == "source" and (commit_message is None or commit_message == ""):
            self.write_error(400)

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
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            server_root_dir=self.root_dir,
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type=repo,
            config=self.config,
        )

        if repo == "release":
            git_service.delete_repo_contents(include_git=True)
            src_path = GitService(
                self.root_dir,
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
            try:
                generator.start()
                self.log.info("GenerateAssignment conversion done")
            except GraderConvertException as e:
                self.log.error("Converting failed: Error converting notebook!", exc_info=True)
                try:
                    msg = e.args[0]
                    assert isinstance(msg, str)
                except (KeyError, AssertionError):
                    msg = "Converting release version failed!"
                raise HTTPError(400, message=msg)
            try:
                gradebook_path = os.path.join(git_service.path, "gradebook.json")
                self.log.info(f"Reading gradebook file: {gradebook_path}")
                with open(gradebook_path, "r") as f:
                    gradebook_json: dict = json.load(f)
            except FileNotFoundError:
                self.log.error(f"Cannot find gradebook file: {gradebook_path}")
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
            git_service.commit(m=commit_message)
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
        # committing might fail because there is nothing to commit -> try to push regardless
        try:
            git_service.push(f"grader_{repo}", force=True)
        except GitError as e:
            self.log.error("GitError:\n" + e.error)
            self.write_error(400)
            return

        if submit and repo == "assignment":
            self.log.info(f"Submitting assignment {assignment_id}!")
            try:
                latest_commit_hash = git_service.get_log(history_count=1)[0]["commit"]
                submission = Submission(commit_hash=latest_commit_hash)
                await self.request_service.request(
                    "POST",
                    f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/submissions",
                    body=submission.to_dict(),
                    header=self.grader_authentication_header,
                )
            except (KeyError, IndexError):
                self.set_status(500)
                self.write_error(500)
                return
            except HTTPClientError as e:
                self.set_status(e.code)
                self.write_error(e.code)
                return

        self.write("OK")


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/reset\/?"
)
class ResetHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int):
        try:
            await self.request_service.request(
                "GET",
                f"{self.base_url}/lectures/{lecture_id}/assignments/{assignment_id}/reset",
                header=self.grader_authentication_header,
            )
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write("OK")


@register_handler(
    path=r"\/(?P<lecture_id>\d*)\/(?P<assignment_id>\d*)\/(?P<notebook_name>.*)"
)
class NotebookAccessHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, notebook_name: str):
        notebook_name = unquote(notebook_name)

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
        except HTTPClientError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        git_service = GitService(
            server_root_dir=self.root_dir,
            lecture_code=lecture["code"],
            assignment_name=assignment["name"],
            repo_type="release",
            config=self.config,
            force_user_repo=True,
        )

        if not git_service.is_git():
            try:
                git_service.init()
                git_service.set_author()
                git_service.set_remote(f"grader_release")
                git_service.pull(f"grader_release", force=True)
                self.write("OK")
            except GitError as e:
                self.log.error("GitError:\n" + e.error)
                self.write_error(400)

        # http://128.130.202.214:8080/user/ubuntu/lab/tree/20wle2/Assignment%201/6%20-%20Truth%20Tables.ipynb
        try:
            username = self.get_current_user()["name"]
        except TypeError as e:
            self.log.error(e)
            self.write_error(403)
            return
        url = f'/user/{username}/lab/tree/{lecture["code"]}/{quote(assignment["name"])}/{quote(notebook_name)}'
        self.log.info(f"Redirecting to {url}")
        self.redirect(url)
