import datetime
import logging
import os
import shlex
import subprocess
from urllib.parse import unquote

from service.handlers.base_handler import GraderBaseHandler
from service.orm.assignment import Assignment
from service.orm.group import Group
from service.orm.lecture import Lecture
from service.orm.submission import Submission
from service.orm.takepart import Role, Scope
from service.registry import VersionSpecifier, register_handler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tornado.ioloop import IOLoop
from tornado.process import Subprocess
from tornado.web import HTTPError, stream_request_body

from service.server import GraderServer


class GitBaseHandler(GraderBaseHandler):
    def initialize(self):
        app: GraderServer = self.application
        self.gitbase = os.path.join(app.grader_service_dir, "git")

    async def data_received(self, chunk: bytes):
        return self.process.stdin.write(chunk)

    def write_error(self, status_code: int, **kwargs) -> None:
        self.clear()
        if status_code == 403 and not self.has_auth:
            status_code = 401
            self.set_header("WWW-Authenticate", 'Basic realm="User Visible Realm"')
        self.set_status(status_code)

    def on_finish(self):
        if hasattr(
            self, "process"
        ):  # if we exit from super prepare (authentication) the process is not created
            if self.process.stdin is not None:
                self.process.stdin.close()
            if self.process.stdout is not None:
                self.process.stdout.close()
            if self.process.stderr is not None:
                self.process.stderr.close()
            IOLoop.current().spawn_callback(self.process.wait_for_exit)

    async def git_response(self):
        try:
            while data := await self.process.stdout.read_bytes(8192, partial=True):
                self.write(data)
                await self.flush()
        except:
            pass

    def gitlookup(self, rpc: str):
        pathlets = self.request.path.strip("/").split("/")
        # pathlets = ['services', 'grader', 'git', 'lecture_code', 'assignment_name', 'repo_type', ...]
        if len(pathlets) < 6:
            return None
        pathlets = pathlets[3:]
        lecture_path = os.path.abspath(os.path.join(self.gitbase, pathlets[0]))
        assignment_path = os.path.abspath(
            os.path.join(self.gitbase, pathlets[0], unquote(pathlets[1]))
        )

        repo_type = pathlets[2]
        if repo_type not in {
            "source",
            "release",
            "assignment",
            "autograde",
            "feedback",
        }:
            return None

        # get lecture and assignment if they exist
        try:
            lecture = (
                self.session.query(Lecture).filter(Lecture.code == pathlets[0]).one()
            )
        except NoResultFound:
            self.error_message = "Not Found"
            raise HTTPError(404)
        except MultipleResultsFound:
            raise HTTPError(400)
        role = self.session.query(Role).get((self.user.name, lecture.id))
        if repo_type == "source" and role.role == Scope.student:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        # no push to release allowed for students
        if (
            repo_type == "release"
            and role.role == Scope.student
            and rpc in ["send-pack", "receive-pack"]
        ):
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        # no push allowed for autograde and feedback -> the autograder executor can push locally so it will not be affected by this
        if repo_type in ["autograde", "feedback"] and rpc in [
            "send-pack",
            "receive-pack",
        ]:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        # no pull allowed for autograde for students
        if (
            repo_type == "autograde"
            and role.role == Scope.student
            and rpc == "upload-pack"
        ):
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        # students should not be able to pull other submissions -> add query param for sub_id
        if (
            repo_type == "feedback"
            and role.role == Scope.student
            and rpc == "upload-pack"
        ):
            try:
                sub_id = int(pathlets[3])
            except (ValueError, IndexError):
                self.error_message = "Unauthorized"
                raise HTTPError(403)
            submission = self.session.query(Submission).get(sub_id)
            if submission is None or submission.username != self.user.name:
                self.error_message = "Unauthorized"
                raise HTTPError(403)

        try:
            assignment = (
                self.session.query(Assignment)
                .filter(
                    Assignment.lectid == lecture.id,
                    Assignment.name == unquote(pathlets[1]),
                )
                .one()
            )
        except NoResultFound:
            self.error_message = "Not Found"
            raise HTTPError(404)
        except MultipleResultsFound:
            raise HTTPError(400)

        if repo_type == "assignment":
            repo_type: str = assignment.type

        # create directories once we know they exist in the database
        if not os.path.exists(lecture_path):
            os.mkdir(lecture_path)
        if not os.path.exists(assignment_path):
            os.mkdir(assignment_path)

        # construct final path from repo type
        if repo_type == "source" or repo_type == "release":
            path = os.path.join(assignment_path, repo_type)
        elif repo_type in ["autograde", "feedback"]:
            type_path = os.path.join(assignment_path, repo_type, assignment.type)
            if assignment.type == "user":
                path = os.path.join(type_path, self.user.name)
            else:
                group = self.session.query(Group).get((self.user.name, lecture.id))
                if group is None:
                    self.error_message = "Not Found"
                    raise HTTPError(404)
                path = os.path.join(type_path, group.name)
        elif repo_type == "user":
            user_path = os.path.join(assignment_path, repo_type)
            path = os.path.join(user_path, self.user.name)
        elif repo_type == "group":
            group = self.session.query(Group).get((self.user.name, lecture.id))
            if group is None:
                self.error_message = "Not Found"
                raise HTTPError(404)
            group_path = os.path.join(assignment_path, repo_type)
            path = os.path.join(group_path, group.name)
        else:
            return None

        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            out = subprocess.run(["git", "rev-parse", "--is-bare-repository"], cwd=path, capture_output=True)
            is_git = out.returncode == 0 and "true" in out.stdout.decode("utf-8")
        except FileNotFoundError:
            is_git = False
        # return git repo
        if os.path.exists(path) and is_git:
            return path
        else:
            os.mkdir(path)
            # this path has to be a git dir -> call git init
            try:
                self.log.info("Running: git init --bare")
                subprocess.run(["git", "init", "--bare", path], check=True)
            except subprocess.CalledProcessError:
                return None
            return path

    @staticmethod
    def _create_path(path):
        if not os.path.exists(path):
            os.mkdir(path)

    def get_gitdir(self, rpc: str):
        """Determine the git repository for this request"""
        gitdir = self.gitlookup(rpc)
        if gitdir is None:
            raise HTTPError(404, "unable to find repository")
        self.log.info("Accessing git at: %s", gitdir)

        return gitdir


@register_handler(path="/.*/git-(.*)", version_specifier=VersionSpecifier.NONE)
@stream_request_body
class RPCHandler(GitBaseHandler):
    """Request handler for RPC calls

    Use this handler to handle example.git/git-upload-pack and example.git/git-receive-pack URLs"""

    async def prepare(self):
        await super().prepare()
        self.rpc = self.path_args[0]
        self.gitdir = self.get_gitdir(rpc=self.rpc)
        self.cmd = f'git {self.rpc} --stateless-rpc "{self.gitdir}"'
        self.log.info(f"Running command: {self.cmd}")
        self.process = Subprocess(
            shlex.split(self.cmd),
            stdin=Subprocess.STREAM,
            stderr=Subprocess.STREAM,
            stdout=Subprocess.STREAM,
        )

    async def post(self, rpc):
        ## Create submission in database
        # pathlets = ['services', 'grader', 'git', 'lecture_code', 'assignment_name', 'repo_type', ...]
        pathlets = self.request.path.strip("/").split("/")
        pathlets = pathlets[3:]
        if pathlets[-1] == "git-receive-pack" and pathlets[-2] == "assignment":
            # get lecture and assignment if they exist
            try:
                lecture = (
                    self.session.query(Lecture)
                    .filter(Lecture.code == pathlets[0])
                    .one()
                )
                assignment = (
                    self.session.query(Assignment)
                    .filter(
                        Assignment.lectid == lecture.id,
                        Assignment.name == unquote(pathlets[1]),
                    )
                    .one()
                )
            except NoResultFound:
                self.error_message = "Not Found"
                raise HTTPError(404)
            except MultipleResultsFound:
                raise HTTPError(400)

            submission = Submission()
            submission.assignid = assignment.id
            submission.date = datetime.datetime.utcnow()
            submission.username = self.user.name
            submission.feedback_available = False

            if assignment.duedate is not None and submission.date > assignment.duedate:
                self.write({"message": "Cannot submit assignment: Past due date!"})
                self.write_error(400)

            await self.git_response()

            try:
                ret = subprocess.run(
                    shlex.split("git rev-parse main"),
                    capture_output=True,
                    cwd=self.gitdir,
                )
                submission.commit_hash = str(ret.stdout, "utf-8").strip()
                submission.auto_status = "not_graded"
                submission.manual_status = "not_graded"
            except subprocess.CalledProcessError as e:
                self.write_error(400)
                return
            except FileNotFoundError as e:
                self.write_error(404)
                return

            self.session.add(submission)
            self.session.commit()

            self.set_header("Content-Type", "application/x-git-%s-result" % rpc)
            self.set_header(
                "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
            )

            self.finish()
        else:
            self.set_header("Content-Type", "application/x-git-%s-result" % rpc)
            self.set_header(
                "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
            )
            await self.git_response()
            self.finish()


@register_handler(path="/.*/info/refs", version_specifier=VersionSpecifier.NONE)
class InfoRefsHandler(GitBaseHandler):
    """Request handler for info/refs

    Use this handler to handle example.git/info/refs?service= URLs"""

    async def prepare(self):
        await super().prepare()
        if self.get_status() != 200:
            return
        self.rpc = self.get_argument("service")[4:]
        self.cmd = f'git {self.rpc} --stateless-rpc --advertise-refs "{self.get_gitdir(self.rpc)}"'
        self.log.info(f"Running command: {self.cmd}")
        self.process = Subprocess(
            shlex.split(self.cmd),
            stdin=Subprocess.STREAM,
            stderr=Subprocess.STREAM,
            stdout=Subprocess.STREAM,
        )

    async def get(self):
        self.set_header("Content-Type", "application/x-git-%s-advertisement" % self.rpc)
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )

        prelude = f"# service=git-{self.rpc}\n0000"
        size = str(hex(len(prelude))[2:].rjust(4, "0"))
        self.write(size)
        self.write(prelude)
        await self.flush()

        await self.git_response()
        self.finish()
