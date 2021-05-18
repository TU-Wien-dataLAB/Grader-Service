from grader.service.handlers.base_handler import GraderBaseHandler
from grader.service.orm.assignment import Assignment
from datetime import datetime
from grader.common.models.error_message import ErrorMessage
from grader.service.orm.lecture import Lecture
from .db_util import *
from unittest.mock import AsyncMock, MagicMock
import asyncio

def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f

@pytest.mark.asyncio 
async def test_prepare(session):  
    f = asyncio.Future()
    f.set_result({"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]})
    async_mock = AsyncMock(return_value={"name": "user99", "groups": ["lecture1__WS21__student", "lecture1__SS21__tutor", "lecture99__SS22__student"]})
    m = MagicMock()
    m.get_current_user_async = async_mock
    m.session = session
    m.prepare = GraderBaseHandler.prepare
    mocked_handler = MagicMock(spec_set=GraderBaseHandler, return_value=m)

    await GraderBaseHandler.prepare(mocked_handler())

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
