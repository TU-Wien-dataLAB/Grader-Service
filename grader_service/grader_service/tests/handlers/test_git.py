# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
from http import HTTPStatus

import pytest

from pathlib import Path

from grader_service.orm.assignment import Assignment
from grader_service.orm.group import Group
from grader_service.orm.submission import Submission
from grader_service.orm.takepart import Role, Scope
from unittest.mock import Mock
from grader_service.handlers.git.server import GitBaseHandler, GitRepoBasePath 
from grader_service.orm.lecture import Lecture
from tornado.web import HTTPError
from .db_util import *


def get_query_side_effect(lid=1, code="ivs21s", a_type="user", scope=Scope.student, group="test_group",
                          username="test_user", a_id=1):
    def query_side_effect(input):
        m = Mock()
        if input is Lecture:
            lecture = Lecture()
            lecture.id = lid
            lecture.code = code
            m.filter.return_value.one.return_value = lecture
        elif input is Assignment:
            assignment = Assignment()
            assignment.id = a_id
            assignment.type = a_type
            m.filter.return_value.one.return_value = assignment
        elif input is Role:
            role = Role()
            role.role = scope
            m.get.return_value = role
        elif input is Group:
            g = Group()
            g.name = group
            m.get.return_value = g
        elif input is Submission:
            sub = Submission()
            sub.username = username
            m.get.return_value = sub
        else:
            m.filter.return_value.one.return_value = None
        return m

    return query_side_effect


def test_git_lookup_instructor(tmpdir):
    """Test if the git repository was created and the path is correct"""
    path = "services/grader/git/iv21s/1/source"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session
    handler_mock.request_pathlet_tail.return_value = pathlets

    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="group", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    constructed_git_dir = GitBaseHandler.construct_git_dir(handler_mock, repo_type="source",
                                                           lecture=sf(Lecture).filter().one(),
                                                           assignment=sf(Assignment).filter().one())
    handler_mock.construct_git_dir = Mock(return_value=constructed_git_dir)

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "send-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD"))  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/source"


def test_git_lookup_release_pull_instructor(tmpdir):
    path = "services/grader/git/iv21s/1/release"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session
    handler_mock.request_pathlet_tail.return_value = pathlets


    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    constructed_git_dir = GitBaseHandler.construct_git_dir(handler_mock, repo_type="release",
                                                           lecture=sf(Lecture).filter().one(),
                                                           assignment=sf(Assignment).filter().one())
    handler_mock.construct_git_dir = Mock(return_value=constructed_git_dir)

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD"))  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/release"


def test_git_lookup_release_push_student_error(tmpdir):
    path = "services/grader/git/iv21s/assign_1/release"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session
    handler_mock.request_pathlet_tail.return_value = pathlets

    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e, pytest.warns(DeprecationWarning):  # some deprecation warning in jupyter_server
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_source_push_student_error_for_source(tmpdir):
    path = "services/grader/git/iv21s/assign_1/source"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    handler_mock.request_pathlet_tail.return_value = pathlets
    # handler_mock.session = session

    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e, pytest.warns(DeprecationWarning):  # some deprecation warning in jupyter_server
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def mock_git_lookup(rpc: str):
    if rpc == "bad":
        return None
    else:
        return "/path/to"


def test_get_gitdir_not_found(tmpdir):
    handler_mock = Mock()
    handler_mock.request.path = "/abc"
    handler_mock.gitlookup = mock_git_lookup
    with pytest.raises(HTTPError) as e:
        GitBaseHandler.get_gitdir(handler_mock, "bad")
    assert e.value.status_code == HTTPStatus.NOT_FOUND


def test_get_gitdir(tmpdir):
    handler_mock = Mock()
    handler_mock.request.path = "/abc"
    handler_mock.gitlookup = mock_git_lookup
    path = GitBaseHandler.get_gitdir(handler_mock, "/abc")
    assert path == "/path/to"


def test_git_lookup_push_autograde_instructor_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_push_autograde_student_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()
    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_push_feedback_instructor_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()
    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_push_feedback_student_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()
    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "send-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_pull_autograde_instructor(tmpdir):
    path = "services/grader/git/iv21s/1/autograde/1"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    handler_mock.request_pathlet_tail.return_value = pathlets

    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    role_mock = Mock()
    role_mock.role = Scope.instructor
    handler_mock.get_role = Mock(return_value=role_mock)
    constructed_git_dir = GitBaseHandler.construct_git_dir(handler_mock, repo_type="autograde",
                                                           lecture=sf(Lecture).filter().one(),
                                                           assignment=sf(Assignment).filter().one(),
                                                           submission=sf(Submission).get())
    handler_mock.construct_git_dir = Mock(return_value=constructed_git_dir)

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD"))  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/autograde/user/test_user"


def test_git_lookup_pull_autograde_student_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    handler_mock.request_pathlet_tail.return_value = path.strip("/").split("/")

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "upload-pack", role, pathlets)
    assert e.value.status_code == 403



@pytest.fixture
def feedback_repo(tmpdir):
    path = "services/grader/git/iv21s/1/feedback/1"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))
    username = "test_user"
    repo_path = GitRepoBasePath(root=git_dir, assignment_id=1,
                                lecture_code="iv21s", repo_type="feedback")
    return { "path": path, "pathlets": pathlets, "git_dir": git_dir,
             "username": username, "repo_path": repo_path }


@pytest.fixture
def feedback_handler_mock(feedback_repo):
    handler_mock = Mock()
    handler_mock.request.path = feedback_repo["path"]
    handler_mock.gitbase = feedback_repo["git_dir"]
    handler_mock.user.name = feedback_repo["username"]
    handler_mock.request_pathlet_tail.return_value = feedback_repo["pathlets"]
    handler_mock.git_repo.repo_type = feedback_repo["repo_path"].repo_type
    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor)
    handler_mock.session.query = Mock(side_effect=sf)
    constructed_git_dir = GitBaseHandler.construct_git_dir(handler_mock, repo_type="feedback",
                                                           lecture=sf(Lecture).filter().one(),
                                                           assignment=sf(Assignment).filter().one())
    handler_mock.construct_git_dir = Mock(return_value=constructed_git_dir)
    return handler_mock



def test_git_lookup_pull_feedback_instructor(feedback_repo,
                                             feedback_handler_mock):
    git_dir = feedback_repo["git_dir"]
    handler_mock = feedback_handler_mock
    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")
    assert lookup_dir is not None
    lookup_path = Path(lookup_dir)
    assert lookup_path.exists()
    assert os.path.exists(os.path.join(lookup_dir, "HEAD"))  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/feedback/user/test_user"


def test_git_lookup_pull_feedback_student_with_valid_id(feedback_repo,
                                                        feedback_handler_mock):

    git_dir = feedback_repo["git_dir"]
    handler_mock = feedback_handler_mock
    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")
    assert lookup_dir is not None
    lookup_path = Path(lookup_dir)
    assert lookup_path.exists()
    assert lookup_path.joinpath("HEAD").exists()  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/feedback/user/test_user"


def test_git_lookup_pull_feedback_student_with_valid_id_extra(tmpdir):
    path = "services/grader/git/iv21s/1/feedback/1/info/refs&service=git-upload-pack"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    handler_mock.request_pathlet_tail.return_value = pathlets

    # orm mocks
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student, username="test_user")
    handler_mock.session.query = Mock(side_effect=sf)
    constructed_git_dir = GitBaseHandler.construct_git_dir(handler_mock, repo_type="feedback",
                                                           lecture=sf(Lecture).filter().one(),
                                                           assignment=sf(Assignment).filter().one())
    handler_mock.construct_git_dir = Mock(return_value=constructed_git_dir)

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD"))  # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/1/feedback/user/test_user"


def test_git_lookup_pull_feedback_student_with_invalid_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback/1"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # test that submission with id 1 comes from "other_user"
    sf = get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student, username="other_user")
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "upload-pack", role, pathlets)
    assert e.value.status_code == 403


# /services/grader/git/20wle2/Assignment%201/feedback/2/info/refs&service=git-upload-pack
def test_git_lookup_pull_feedback_student_no_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "upload-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_pull_feedback_student_no_id_error_extra():
    path = "/services/grader/git/20wle2/Assignment%201/feedback/info/refs&service=git-upload-pack"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "upload-pack", role, pathlets)
    assert e.value.status_code == 403


def test_git_lookup_pull_feedback_student_bad_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback/abc/"
    pathlets = path.strip("/").split("/")[3:]
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    sf = get_query_side_effect(code="iv21s", scope=Scope.student)
    handler_mock.session.query = Mock(side_effect=sf)
    role = sf(Role).get()

    with pytest.raises(HTTPError) as e:
        GitBaseHandler._check_git_repo_permissions(handler_mock, "upload-pack", role, pathlets)
    assert e.value.status_code == 403
