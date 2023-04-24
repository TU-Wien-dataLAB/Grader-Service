# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import shlex
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
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
    root: str
    lecture_code: str
    assignment_id: int
    repo_type: str

    def __repr__(self):
        return f"{self.root}/{self.lecture_code}/{self.assignment_id}/{self.repo_type}" # noqa E501


class GitRepoSubmissionExtendedPath(GitRepoBasePath):
    # edit repo, feedback
    def __init__(self, root: str, lecture_code: str,
                 assignment_id: int, repo_type: str,
                 submission_id: int):
        super().__init__(root, lecture_code, assignment_id, repo_type)
        self.submission_id = submission_id

    def __repr__(self):
        return f"{self.root}/{self.lecture_code}/{self.assignment_id}/{self.repo_type}/{self.submission_id}" # noqa E501


class GitRepoUserExtendedPath(GitRepoBasePath):

    def __init__(self, root: str, lecture_code: str,
                 assignment_id: int, repo_type: str,
                 username: str):
        super().__init__(root, lecture_code, assignment_id, repo_type)
        self.username = username

    def __repr__(self):
        return f"{self.root}/{self.lecture_code}/{self.assignment_id}/{self.repo_type}/{self.username}" # noqa E501


class RepoTypeToken(Enum):
    SOURCE = auto()  # WE DO NOTHING
    RELEASE = auto()  # WE DO NOTHING
    ASSIGNMENT = auto()
    EDIT = auto()  # + SUBMISSION ID
    AUTOGRADE = auto()  # + USERNAME
    FEEDBACK = auto()  # + SUBMISSION ID
    USER = auto()  # + USERNAME
    GROUP = auto()  # + USERNAME
    INVALID = auto()


def str_to_repo_type_token(repo_type: str) -> RepoTypeToken:
    if repo_type == "source":
        return RepoTypeToken.SOURCE
    elif repo_type == "release":
        return RepoTypeToken.RELEASE
    elif repo_type == "assignment":
        return RepoTypeToken.ASSIGNMENT
    elif repo_type == "edit":
        return RepoTypeToken.EDIT
    elif repo_type == "autograde":
        return RepoTypeToken.AUTOGRADE
    elif repo_type == "feedback":
        return RepoTypeToken.FEEDBACK
    elif repo_type == "user":
        return RepoTypeToken.USER
    elif repo_type == "group":
        return RepoTypeToken.GROUP
    else:
        return RepoTypeToken.INVALID


class GitBaseHandler(GraderBaseHandler):

    # TODO: list all attributes and methods here
    # Possibly: pathlets, git_repo, lecture, assignment

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
                                    pathlets: List[str]):
        repo_type = pathlets[2]

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
                    sub_id = int(pathlets[3])
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
        self.set_git_repo()
        self.set_repo_type_token()
        if not self.is_valid_repo_type(self.repo_type_token):
            return None
        self.query_and_set_lecture()
        self.mk_lecture_path()
        self.query_and_set_assignment()
        self.mk_assignment_path()
        self.query_and_set_role()
        pathlets = self.request_pathlet_tail()
        self._check_git_repo_permissions(rpc, self.role, pathlets)
        if self.repo_type_token is RepoTypeToken.ASSIGNMENT:
            self.update_repo_type_assignment()
        self.query_and_set_submission()
        # Note: from this point on we seem to be calling out to the
        #       base_handler module
        path = self.construct_git_dir(self.git_repo.repo_type, self.lecture,
                                      self.assignment,
                                      submission=self.submission)
        if path is None:
            return None
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not ((os.path.exists(path)) and (self.is_base_git_dir(path))):
            os.mkdir(path)
            try:
                self.log.info("Running: git init --bare")
                subprocess.run(["git", "init", "--bare", path], check=True)
            except subprocess.CalledProcessError:
                return None
            if (self.repo_type_token is RepoTypeToken.USER
                    or self.repo_type_token is RepoTypeToken.GROUP):
                # We're dealing with a release
                repo_path_release = self.construct_git_dir(
                        'release', self.assignment.lecture, self.assignment)
                err_msg = "Error: expceted path or str, got None"
                assert repo_path_release is not None, err_msg
                if not os.path.exists(repo_path_release):
                    return None
                self.duplicate_release_repo(
                    repo_path_release=repo_path_release, repo_path_user=path,
                    assignment=self.assignment, message="Init with Release",
                    checkout_main=True)
        self.write_pre_receive_hook(path)
        return path

    def route_to_list(self):
        request_route_list = self.request.path.strip("/").split("/")
        assert request_route_list is not None, "Error, can not be none"
        return request_route_list

    def get_index_last_git_pathlet(self):
        request_route_list = self.route_to_list()
        plist = request_route_list.copy()
        plist.reverse()
        try:
            return_index = len(plist) - plist.index("git")
        except ValueError:
            raise HTTPError(400, "Invalid git path used in request")
        return return_index

    def request_pathlet_tail(self):
        index_last_git_pathlet = self.get_index_last_git_pathlet()
        request_route_list = self.route_to_list()
        trimmed_list = request_route_list[index_last_git_pathlet:]
        num_expected_pathlets = 6
        assert len(trimmed_list) < num_expected_pathlets, \
            f"Error: expected {num_expected_pathlets} got {len(trimmed_list)}"
        return request_route_list[index_last_git_pathlet:]

    def set_git_repo(self):
        "Set the git_repo attribute"
        pathlets = self.request_pathlet_tail()
        git_repo_base_path = GitRepoBasePath(
                root=self.gitbase, lecture_code=pathlets[0],
                assignment_id=int(pathlets[1]), repo_type=pathlets[2])
        rt_tok = str_to_repo_type_token(git_repo_base_path.repo_type)
        if rt_tok is RepoTypeToken.EDIT or rt_tok is RepoTypeToken.FEEDBACK:
            git_repo_base_path = GitRepoSubmissionExtendedPath(
                root=git_repo_base_path.root,
                lecture_code=git_repo_base_path.lecture_code,
                assignment_id=git_repo_base_path.assignment_id,
                repo_type=git_repo_base_path.repo_type,
                submission_id=int(pathlets[3]))
        elif ((rt_tok is RepoTypeToken.USER) or (rt_tok is RepoTypeToken.GROUP)
              or (rt_tok is RepoTypeToken.AUTOGRADE)):
            git_repo_base_path = GitRepoUserExtendedPath(
                root=git_repo_base_path.root,
                lecture_code=git_repo_base_path.lecture_code,
                assignment_id=git_repo_base_path.assignment_id,
                repo_type=git_repo_base_path.repo_type,
                username=pathlets[3])
        self.git_repo = git_repo_base_path

    def set_repo_type_token(self):
        "Set attribute"
        self.repo_type_token = str_to_repo_type_token(self.git_repo.repo_type)

    def update_repo_type_assignment(self):
        new_git_repo = deepcopy(self.git_repo)
        new_git_repo.repo_type = str(self.assignment.type)
        self.git_repo = new_git_repo
        self.set_repo_type_token()

    def query_and_set_lecture(self):
        lecture_code = self.git_repo.lecture_code
        try:
            lecture = (
                self.session.query(
                    Lecture).filter(Lecture.code == lecture_code).one()
                )
        except NoResultFound:
            raise HTTPError(404, reason="Lecture was not found")
        except MultipleResultsFound:
            raise HTTPError(500, reason="Found more than one lecture")
        self.lecture = lecture

    def mk_lecture_path(self):
        pathlets = self.request_pathlet_tail()
        lecture_path = os.path.abspath(os.path.join(self.gitbase, pathlets[0]))
        if not os.path.exists(lecture_path):
            os.mkdir(lecture_path)

    def query_and_set_assignment(self):
        try:
            assignment = self.get_assignment(
                    self.lecture.id, self.git_repo.assignment_id)
        except ValueError:
            raise HTTPError(404, "Assignment not found")
        self.assignment = assignment

    def mk_assignment_path(self):
        pathlets = self.request_pathlet_tail()
        assignment_path = os.path.abspath(
            os.path.join(self.gitbase, pathlets[0], pathlets[1]))
        if not os.path.exists(assignment_path):
            os.mkdir(assignment_path)

    def query_and_set_role(self):
        # TODO: should we check and return errors here?
        self.role = self.session.query(Role).get((self.user.name,
                                                  self.lecture.id))

    def query_and_set_submission(self):
        submission = None
        pathlets = self.request_pathlet_tail()
        if ((self.repo_type_token is RepoTypeToken.AUTOGRADE)
                or (self.repo_type_token is RepoTypeToken.FEEDBACK)
                or (self.repo_type_token is RepoTypeToken.EDIT)):
            try:
                sub_id = int(pathlets[3])
            except (ValueError, IndexError):
                raise HTTPError(403)
            submission = self.session.query(Submission).get(sub_id)
        self.submission = submission

    def is_valid_repo_type(self, repo_type_token: RepoTypeToken) -> bool:
        if repo_type_token is RepoTypeToken.INVALID:
            return False
        return True

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
    def _get_hook_file_allow_pattern(extensions: Optional[List[str]] = None) -> str:  # noqa E501
        pattern = ""
        if extensions is None:
            req_handler_conf = RequestHandlerConfig.instance()
            extensions = req_handler_conf.git_allowed_file_extensions
        elif len(extensions) > 0:
            allow_patterns = ["\\." + s.strip(".").replace(".", "\\.") for s in extensions]  # noqa E501
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
