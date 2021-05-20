import json
from grader.service.handlers.base_handler import GraderBaseHandler
from grader.service.orm.assignment import Assignment
from datetime import datetime
from grader.common.models.error_message import ErrorMessage
from grader.service.orm.lecture import Lecture
from .db_util import *
from unittest.mock import AsyncMock, MagicMock, Mock
import asyncio

@pytest.mark.asyncio
async def test_authenticate_token_user_None():
    token = "test_token"
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]}
    user_mock = AsyncMock(return_value=user)
    # token_mock = Mock(return_value="test_token")
    m = MagicMock()
    m.application.max_token_cookie_age_days = 0.05
    m.get_current_user_async = user_mock
    # m.session = session
    m.get_secure_cookie = Mock(return_value=None)
    m.authenticate_token_user = GraderBaseHandler.authenticate_token_user
    await GraderBaseHandler.authenticate_token_user(m, token)
    m.set_secure_cookie.assert_called_with(token, json.dumps(user), expires_days=0.05)

@pytest.mark.asyncio
async def test_authenticate_token_user_Present():
    token = "test_token"
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]}
    user_mock = AsyncMock(return_value=user)
    # token_mock = Mock(return_value="test_token")
    m = MagicMock()
    m.application.max_token_cookie_age_days = 0.05
    m.get_current_user_async = user_mock
    # m.session = session
    m.get_secure_cookie = Mock(return_value=json.dumps(user))
    m.authenticate_token_user = GraderBaseHandler.authenticate_token_user
    await GraderBaseHandler.authenticate_token_user(m, token)
    with pytest.raises(AssertionError):
        m.set_secure_cookie.assert_called_with(token, json.dumps(user), expires_days=0.05)

def test_authenticate_cookie_user_None():
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]}
    m = MagicMock()
    m.application.max_user_cookie_age_days = 1
    m.get_secure_cookie = Mock(return_value=None)
    m.authenticate_cookie_user = GraderBaseHandler.authenticate_cookie_user
    assert not GraderBaseHandler.authenticate_cookie_user(m, user)
    m.set_secure_cookie.assert_called_with(user["name"], json.dumps(user), expires_days=1)


def test_authenticate_cookie_user_Identical():
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]}
    m = MagicMock()
    m.application.max_user_cookie_age_days = 1
    m.get_secure_cookie = Mock(return_value=json.dumps(user))
    m.authenticate_cookie_user = GraderBaseHandler.authenticate_cookie_user
    assert GraderBaseHandler.authenticate_cookie_user(m, user)
    with pytest.raises(AssertionError):
        m.set_secure_cookie.assert_called_with(user["name"], json.dumps(user), expires_days=1)

def test_authenticate_cookie_user_New():
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]}
    m = MagicMock()
    m.application.max_user_cookie_age_days = 1
    old_user = user.copy()
    old_user["groups"] = ["lecture1__WS21__student", "lecture1__SS21__tutor"]
    m.get_secure_cookie = Mock(return_value=json.dumps(old_user))
    m.authenticate_cookie_user = GraderBaseHandler.authenticate_cookie_user
    assert not GraderBaseHandler.authenticate_cookie_user(m, user)
    m.set_secure_cookie.assert_called_with(user["name"], json.dumps(user), expires_days=1)

@pytest.mark.asyncio 
async def test_authenticate_user_no_cookies(session):
    token = "test_token"
    user = {"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]} 
    async_mock = AsyncMock(return_value=user)
    m = MagicMock()
    m.get_current_user_async = async_mock
    m.session = session
    m.authenticate_user = GraderBaseHandler.authenticate_user
    m.get_request_token = Mock(return_value=token)
    m.authenticate_token_user = async_mock
    m.authenticate_cookie_user = Mock(return_value=False)

    await GraderBaseHandler.authenticate_user(m)

    lecture99 = session.query(Lecture).filter(Lecture.name == "lecture99").one_or_none()
    assert lecture99 is not None


def test_string_serialization():
    assert GraderBaseHandler._serialize("test") == "test"


def test_number_serialization():
    assert GraderBaseHandler._serialize(1) == 1
    assert GraderBaseHandler._serialize(2.5) == 2.5


def test_list_serialization():
    assert GraderBaseHandler._serialize([1, 2, 3]) == [1, 2, 3]

def test_list_serialization_empty():
    assert GraderBaseHandler._serialize([]) == []

def test_tuple_serialization():
    assert GraderBaseHandler._serialize((1, 2, 3)) == (1, 2, 3)


def test_dict_serialization():
    d = {"a": 1, "b": "test", 5: 6}
    s = GraderBaseHandler._serialize(d)
    assert d == s

def test_dict_serialization_empty():
    d = {}
    s = GraderBaseHandler._serialize(d)
    assert d == s

def test_datetime_serialization():
    d = datetime.now()
    s = GraderBaseHandler._serialize(d)
    assert type(s) == str
    assert str(d) == s

def test_assignment_serialization():
    d = {
        "id": 1,
        "name": "test",
        "due_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "status": "created",
        "exercises": [],
        "files": []
    }
    a = Assignment(
        id=d["id"],
        name=d["name"],
        lectid=1,
        duedate=d["due_date"],
        points=0,
        status=d["status"],
    )

    assert GraderBaseHandler._serialize(a) == d

def test_nested_serialization():
    o = [{"b": None}, {"a": 2}, "test", {"z": []}]
    s = GraderBaseHandler._serialize(o)
    assert o == s

def test_api_model_serialization():
    err = ErrorMessage("")
