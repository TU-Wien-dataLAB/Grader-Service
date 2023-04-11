# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import shlex
import subprocess
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from string import Template
from typing import List, Optional

from grader_service.handlers.base_handler import (GraderBaseHandler,
                                                  RequestHandlerConfig)
from grader_service.orm.lecture import Lecture
from grader_service.orm.submission import Submission
from grader_service.orm.takepart import Role, Scope
from grader_service.registry import VersionSpecifier, register_handler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tornado.ioloop import IOLoop
from tornado.process import Subprocess
from tornado.web import HTTPError, stream_request_body


@dataclass
class GitRepoBasePath:
    lecture_code: str
    assignment_id: int
    repo_type: str


@dataclass
class GitRepoSubmissionExtendedPath(GitRepoBasePath):
    submission_id: int

    def __init__(self, git_repo_base_path, submission_id: int):
        self.lecture_code = git_repo_base_path.lecture_code
        self.assignment_id = git_repo_base_path.assignment_id
        self.repo_type = git_repo_base_path.repo_type
        self.submission_id = submission_id


@dataclass
class GitRepoUserExtendedPath(GitRepoBasePath):
    username: str

    def __init__(self, git_repo_base_path, username: str):
        self.lecture_code = git_repo_base_path.lecture_code
        self.assignment_id = git_repo_base_path.assignment_id
        self.repo_type = git_repo_base_path.repo_type
        self.username = username


class RepoType(StrEnum):
    SOURCE = auto()  # WE DO NOTHING
    RELEASE = auto()  # WE DO NOTHING
    EDIT = auto()  # + SUBMISSION ID
    AUTOGRADE = auto()  # + USERNAME
    FEEDBACK = auto()  # + SUBMISSION ID
    USER = auto()  # + USERNAME
    GROUP = auto()  # + USERNAME


class GitBaseHandler(GraderBaseHandler):

    async def data_received(self, chunk: bytes):
        return self.process.stdin.write(chunk)

    def write_error(self, status_code: int, **kwargs) -> None:
        self.clear()
        if status_code == 401:
            self.set_header("WWW-Authenticate",
                            'Basic realm="User Visible Realm"')
        self.set_status(status_code)

    def on_finish(self):
        if hasattr(
                self, "process"
        ):  # if we exit super prepare (authentication) process is not created
            if self.process.stdin is not None:
                self.process.stdin.close()
            if self.process.stdout is not None:
                self.process.stdout.close()
            if self.process.stderr is not None:
                self.process.stderr.close()
            IOLoop.current().spawn_callback(self.process.wait_for_exit)

    async def git_response(self):
        try:
            while data := await self.process.stdout.read_bytes(8192,
                                                               partial=True):
                self.write(data)
                await self.flush()
        except Exception as e:
            print(f"Error from git response {e}")

    def _check_git_repo_permissions(self, rpc: str, role: Role,
                                    git_repo_base_path):
        repo_type = git_repo_base_path.repo_type

        if role.role == Scope.student:
            # 1. no source or release interaction with source repo for students
            # 2. no pull allowed for autograde for students
            if ((repo_type in ["source", "release", "edit"])
                    or (repo_type == "autograde" and rpc == "upload-pack")):
                raise HTTPError(403)

            # 3. students should not be able to pull other submissions
            #    -> add query param for sub_id
            if (repo_type == "feedback") and (rpc == "upload-pack"):
                try:
                    sub_id = int(git_repo_base_path.submission_id)
                except (ValueError, IndexError):
                    raise HTTPError(403)
                submission = self.session.query(Submission).get(sub_id)
                if submission is None or submission.username != self.user.name:
                    raise HTTPError(403)

        # 4. no push allowed for autograde and feedback
        #    -> the autograder executor can push locally (will bypass this)
        if ((repo_type in ["autograde", "feedback"])
                and (rpc in ["send-pack", "receive-pack"])):
            raise HTTPError(403)

    def gitlookup(self, rpc: str):
        request_route_list = self.split_route_to_list()
        git_route_tail = self.get_git_route_tail(request_route_list)

        git_base_path = self.make_git_base_path(git_route_tail)
        assert isinstance(git_base_path, GitRepoBasePath), "Error: constructor"
        # request_route_list = ['services', 'grader', 'git',
        #             'lecture_code', 'assignment_id', 'repo_type', ...]

        # get lecture and assignment if they exist
        lecture = self.get_lecture(git_base_path.lecture_code)
        assignment = self.get_assignment(git_base_path.assignment_id)

        role = self.session.query(Role).get((self.user.name, lecture.id))
        self._check_git_repo_permissions(rpc, role, git_base_path)

        # TODO refactor from here
        repo_type = git_base_path.repo_type

        if repo_type == "assignment":
            repo_type: str = assignment.type

        # create directories once we know they exist in the database
        if not os.path.exists(lecture_path):
            os.mkdir(lecture_path)
        if not os.path.exists(assignment_path):
            os.mkdir(assignment_path)

        submission = None
        if repo_type in ["autograde", "feedback", "edit"]:
            try:
                sub_id = int(pathlets[3])
            except (ValueError, IndexError):
                raise HTTPError(403)
            submission = self.session.query(Submission).get(sub_id)

        path = self.construct_git_dir(repo_type, lecture, assignment,
                                      submission=submission)
        if path is None:
            return None

        os.makedirs(os.path.dirname(path), exist_ok=True)
        is_git = self.is_base_git_dir(path)
        # return git repo
        if os.path.exists(path) and is_git:
            self.write_pre_receive_hook(path)
            return path
        else:
            os.mkdir(path)
            # this path has to be a git dir -> call git init
            try:
                self.log.info("Running: git init --bare")
                subprocess.run(["git", "init", "--bare", path], check=True)
            except subprocess.CalledProcessError:
                return None

            if repo_type in ["user", "group"]:
                repo_path_release = self.construct_git_dir('release',
                                                           assignment.lecture,
                                                           assignment)
                safe_repo_path_release = repo_path_release
                err_msg = "Error: expceted path or str, got None"
                assert safe_repo_path_release is not None, err_msg
                if not os.path.exists(safe_repo_path_release):
                    return None
                self.duplicate_release_repo(
                    repo_path_release=safe_repo_path_release,
                    repo_path_user=path,
                    assignment=assignment,
                    message="Initialize with Release",
                    checkout_main=True)

            self.write_pre_receive_hook(path)
            return path

    def split_route_to_list(self):
        request_route_list = self.request.path.strip("/").split("/")
        assert request_route_list is not None, "Error: can not be None"
        num_expected_sub_paths = 6
        assert len(request_route_list) < num_expected_sub_paths, \
            f"Error: can not be smaller than {num_expected_sub_paths}"
        return request_route_list

    def write_pre_receive_hook(self, path: str):
        hook_dir = os.path.join(path, "hooks")
        if not os.path.exists(hook_dir):
            os.mkdir(hook_dir)

        hook_file = os.path.join(hook_dir, "pre-receive")
        if not os.path.exists(hook_file):
            tpl = Template(self._read_hook_template())
            hook = tpl.safe_substitute({
                "tpl_max_file_size": self._get_hook_max_file_size(),
                "tpl_file_extensions": self._get_hook_file_allow_pattern(),
                "tpl_max_file_count": self._get_hook_max_file_count()
            })
            with open(hook_file, "wt") as f:
                os.chmod(hook_file, 0o755)
                f.write(hook)

    @staticmethod
    def _get_hook_file_allow_pattern(
            extensions: Optional[List[str]] = None) -> str:  # noqa E501
        pattern = ""
        if extensions is None:
            req_handler_conf = RequestHandlerConfig.instance()
            extensions = req_handler_conf.git_allowed_file_extensions
        elif len(extensions) > 0:
            allow_patterns = ["\\." + s.strip(".").replace(".", "\\.") for s in
                              extensions]  # noqa E501
            pattern = "|".join(allow_patterns)
        return pattern

    @staticmethod
    def _get_hook_max_file_size():
        return RequestHandlerConfig.instance().git_max_file_size_mb

    @staticmethod
    def _get_hook_max_file_count():
        return RequestHandlerConfig.instance().git_max_file_count

    @staticmethod
    def _read_hook_template() -> str:
        file_path = Path(__file__).parent / "hook_templates" / "pre-receive"
        with open(file_path, mode="rt") as f:
            return f.read()

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

    def get_git_route_tail(self, request_route_list):
        index = None
        for i in range(0, len(request_route_list) - 1):
            if request_route_list[i] == 'git':
                index = i
        return request_route_list[index:]

    def make_git_base_path(self, git_route_tail):
        git_repo_base_path = GitRepoBasePath(
            lecture_code=git_route_tail[0],
            assignment_id=int(git_route_tail[1]),
            repo_type=git_route_tail[2]
        )
        if ((git_repo_base_path.repo_type == RepoType.EDIT)
                or (git_repo_base_path.repo_type == RepoType.FEEDBACK)):
            git_repo_base_path = GitRepoSubmissionExtendedPath(
                git_repo_base_path,
                submission_id=int(git_route_tail[3])
            )
        elif ((git_repo_base_path.repo_type == RepoType.USER)
              or (git_repo_base_path.repo_type == RepoType.GROUP)
              or (git_repo_base_path.repo_type == RepoType.AUTOGRADE)):
            git_repo_base_path = GitRepoUserExtendedPath(
                git_repo_base_path,
                username=git_route_tail[3]
            )
        return git_repo_base_path


@register_handler(path="/.*/git-(.*)", version_specifier=VersionSpecifier.NONE)
@stream_request_body
class RPCHandler(GitBaseHandler):
    """Request handler for RPC calls

    Use this handler to handle example.git/git-upload-pack
    and example.git/git-receive-pack URLs"""

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
        self.set_header("Content-Type", "application/x-git-%s-result" % rpc)
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
        await self.git_response()
        await self.finish()


@register_handler(path="/.*/info/refs",
                  version_specifier=VersionSpecifier.NONE)
class InfoRefsHandler(GitBaseHandler):
    """Request handler for info/refs

    Use this handler to handle example.git/info/refs?service= URLs"""

    async def prepare(self):
        await super().prepare()
        if self.get_status() != 200:
            return
        self.rpc = self.get_argument("service")[4:]
        self.cmd = f'git {self.rpc} --stateless-rpc --advertise-refs "{self.get_gitdir(self.rpc)}"'  # noqa E501
        self.log.info(f"Running command: {self.cmd}")
        self.process = Subprocess(
            shlex.split(self.cmd),
            stdin=Subprocess.STREAM,
            stderr=Subprocess.STREAM,
            stdout=Subprocess.STREAM,
        )

    async def get(self):
        self.set_header("Content-Type",
                        "application/x-git-%s-advertisement" % self.rpc)
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )

        prelude = f"# service=git-{self.rpc}\n0000"
        size = str(hex(len(prelude))[2:].rjust(4, "0"))
        self.write(size)
        self.write(prelude)
        await self.flush()

        await self.git_response()
        await self.finish()
