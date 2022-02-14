from grader_service.orm.assignment import Assignment
from grader_service.orm.group import Group
from grader_service.orm.submission import Submission
from grader_service.orm.takepart import Role, Scope
import pytest
from unittest.mock import Mock
from grader_service.handlers.git.server import GitBaseHandler
from grader_service.orm.lecture import Lecture
from tornado.web import HTTPError
from .db_util import *
import os


def get_query_side_effect(lid=1, code="ivs21s", a_type="user", scope=Scope.student, group="test_group", username="test_user"):
    def query_side_effect(input):
        m = Mock()
        if input is Lecture:
            lecture = Lecture()
            lecture.id = lid
            lecture.code = code
            m.filter.return_value.one.return_value = lecture
        elif input is Assignment:
            assignment = Assignment()
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


def test_git_lookup_student(tmpdir):
    path = "services/grader/git/iv21s/assign_1/assignment"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, rpc="send-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/user/test_user"


def test_git_lookup_group(tmpdir):
    path = "services/grader/git/iv21s/assign_1/assignment"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="group", scope=Scope.student, group="test_group"))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "send-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/group/test_group"


def test_git_lookup_instructor(tmpdir):
    path = "services/grader/git/iv21s/assign_1/source"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="group", scope=Scope.instructor))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "send-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/source"


def test_git_lookup_release_pull_student(tmpdir):
    path = "services/grader/git/iv21s/assign_1/release"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/release"


def test_git_lookup_release_pull_instructor(tmpdir):
    path = "services/grader/git/iv21s/assign_1/release"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/release"


def test_git_lookup_release_push_student_error(tmpdir):
    path = "services/grader/git/iv21s/assign_1/release"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"
    # handler_mock.session = session

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student))

    with pytest.raises(HTTPError), pytest.warns(DeprecationWarning): # some deprecation warning in jupyter_server
        GitBaseHandler.gitlookup(handler_mock, "send-pack")


def test_git_lookup_push_autograde_instructor_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.instructor))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "send-pack")

def test_git_lookup_push_autograde_student_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "send-pack")


def test_git_lookup_push_feedback_instructor_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.instructor))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "send-pack")

def test_git_lookup_push_feedback_student_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "send-pack")

def test_git_lookup_pull_autograde_instructor(tmpdir):
    path = "services/grader/git/iv21s/assign_1/autograde"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/autograde/user/test_user"


def test_git_lookup_pull_autograde_student_error():
    path = "services/grader/git/iv21s/assign_1/autograde"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "upload-pack")


def test_git_lookup_pull_feedback_instructor(tmpdir):
    path = "services/grader/git/iv21s/assign_1/feedback"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.instructor))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/feedback/user/test_user"

def test_git_lookup_pull_feedback_student_with_valid_id(tmpdir):
    path = "services/grader/git/iv21s/assign_1/feedback/1"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student, username="test_user"))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/feedback/user/test_user"


def test_git_lookup_pull_feedback_student_with_valid_id_extra(tmpdir):
    path = "services/grader/git/iv21s/assign_1/feedback/1/info/refs&service=git-upload-pack"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # orm mocks    
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student, username="test_user"))

    lookup_dir = GitBaseHandler.gitlookup(handler_mock, "upload-pack")

    assert os.path.exists(lookup_dir)
    assert os.path.exists(os.path.join(lookup_dir, "HEAD")) # is git dir
    common_path = os.path.commonpath([git_dir, lookup_dir])
    created_paths = os.path.relpath(lookup_dir, common_path)
    assert created_paths == "iv21s/assign_1/feedback/user/test_user"

def test_git_lookup_pull_feedback_student_with_invalid_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback/1"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    # test that submission with id 1 comes from "other_user"
    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", a_type="user", scope=Scope.student, username="other_user"))

    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "upload-pack")

# /services/grader/git/20wle2/Assignment%201/feedback/2/info/refs&service=git-upload-pack
def test_git_lookup_pull_feedback_student_no_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "upload-pack")


def test_git_lookup_pull_feedback_student_no_id_error_extra():
    path = "/services/grader/git/20wle2/Assignment%201/feedback/info/refs&service=git-upload-pack"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "upload-pack")

def test_git_lookup_pull_feedback_student_bad_id_error():
    path = "services/grader/git/iv21s/assign_1/feedback/abc/"
    git_dir = "/tmp"

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    handler_mock.user.name = "test_user"

    handler_mock.session.query= Mock(side_effect=get_query_side_effect(code="iv21s", scope=Scope.student))
    with pytest.raises(HTTPError):
        GitBaseHandler.gitlookup(handler_mock, "upload-pack")