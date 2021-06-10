import json
from grader.service.orm.assignment import Assignment
from grader.service.orm.lecture import Lecture
from grader.service.orm.takepart import Role, Scope
from grader.service.orm.group import Group
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tornado.web import RequestHandler, stream_request_body, HTTPError, Application
from tornado.options import define, options, parse_command_line
from tornado.process import Subprocess
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
import shlex
from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
import os
import subprocess
from grader.service.server import GraderServer


import logging

logger = logging.getLogger(__name__)


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
            self.set_header('WWW-Authenticate', 'Basic realm="User Visible Realm"')
        self.set_status(status_code)

    def on_finish(self):
        if hasattr(self, 'process'): # if we exit from super prepare (authentication) the process is not created
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

    def gitlookup(self):
        pathlets = self.request.path.strip("/").split("/")
        # pathlets = ['services', 'grader', 'git', 'lecture_code', 'assignment_repo', ...]
        pathlets = pathlets[3:]
        lecture_path = os.path.abspath(os.path.join(self.gitbase, pathlets[0]))
        assignment_path = os.path.abspath(os.path.join(self.gitbase, pathlets[0], pathlets[1]))
        
        # get lecture and assignment if they exist
        try:
            lecture = self.session.query(Lecture).filter(Lecture.code == pathlets[0]).one()
        except NoResultFound:
            self.error_message = "Not Found"
            raise HTTPError(404)
        except MultipleResultsFound:
            raise HTTPError(400)
        role = self.session.query(Role).get((self.user.name, lecture.id))
        if role.role == Scope.instructor or role.role == Scope.tutor: # TODO: should tutors have access? probably...
            repo_type: str = "instructor"
        else:
            try:
                assignment = self.session.query(Assignment).filter(Assignment.lectid == lecture.id, Assignment.name == pathlets[1]).one()
            except NoResultFound:
                self.error_message = "Not Found"
                raise HTTPError(404)
            except MultipleResultsFound:
                raise HTTPError(400)
            repo_type: str = assignment.type
        
        # create directories once we know they exist in the database
        if not os.path.exists(lecture_path):
            os.mkdir(lecture_path)
        if not os.path.exists(assignment_path):
            os.mkdir(assignment_path)

        # construct final path from repo type
        if repo_type == "instructor":
            path = os.path.join(assignment_path, repo_type)
        elif repo_type == "user":
            user_path = os.path.join(assignment_path, repo_type)
            if not os.path.exists(user_path):
                os.mkdir(user_path)
            path = os.path.join(user_path, self.user.name)
        elif repo_type == "group":
            group = self.session.query(Group).get((self.user.name, lecture.id))
            if group is None:
                self.error_message = "Not Found"
                raise HTTPError(404)
            group_path = os.path.join(assignment_path, "group")
            if not os.path.exists(group_path):
                os.mkdir(group_path)
            path = os.path.join(group_path, group.name)
        else:
            return None

        # return git repo
        if os.path.exists(path):
            return path
        else:
            os.mkdir(path)
            # this path has to be a git dir -> call git init
            try:
                subprocess.run(["git", "init", "--bare", path], check=True)
            except subprocess.CalledProcessError:
                return None
            return path

    def get_gitdir(self):
        """Determine the git repository for this request"""
        gitdir = self.gitlookup()
        if gitdir is None:
            raise HTTPError(404, "unable to find repository")
        logger.debug("Accessing git at: %s", gitdir)

        return gitdir


@register_handler(path="/.*/git-(.*)")
@stream_request_body
class RPCHandler(GitBaseHandler):
    """Request handler for RPC calls

    Use this handler to handle example.git/git-upload-pack and example.git/git-receive-pack URLs"""

    async def prepare(self):
        await super().prepare()
        self.rpc = self.path_args[0]
        self.cmd = f"git {self.rpc} --stateless-rpc {self.get_gitdir()}"
        self.process = Subprocess(
            shlex.split(self.cmd),
            stdin=Subprocess.STREAM,
            stderr=Subprocess.STREAM,
            stdout=Subprocess.STREAM,
        )

    async def post(self, rpc):
        self.set_header("Content-Type", "application/x-git-%s-result" % rpc)
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        await self.git_response()
        self.finish()


@register_handler(path="/.*/info/refs")
class InfoRefsHandler(GitBaseHandler):
    """Request handler for info/refs

    Use this handler to handle example.git/info/refs?service= URLs"""

    async def prepare(self):
        await super().prepare()
        self.rpc = self.get_argument("service")[4:]
        self.cmd = f"git {self.rpc} --stateless-rpc --advertise-refs {self.get_gitdir()}"
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
