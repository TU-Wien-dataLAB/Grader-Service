import pytest
from unittest.mock import Mock
from grader.service.handlers.git.server import GitBaseHandler
from grader.service.orm.lecture import Lecture
from sqlalchemy.orm import query
from .db_util import *
import os


def test_git_lookup_instructor(session, tmpdir):
    path = "services/grader/git/iv21s/assign_1"
    git_dir = str(tmpdir.mkdir("git"))

    handler_mock = Mock()
    handler_mock.request.path = path
    handler_mock.gitbase = git_dir
    # handler_mock.session = session

    # orm mocks
    query_lecture_mock = Mock()
    lecture = Lecture()
    lecture.id = 1
    lecture.code = "ivs21s"
    query_lecture_mock.filter.return_value.one.return_value = lecture
    handler_mock.session.query = query_lecture_mock

    lookup_dir = GitBaseHandler.gitlookup(handler_mock)

    assert os.path.exists(lookup_dir)
