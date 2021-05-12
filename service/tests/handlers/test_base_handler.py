from grader.service.handlers.base_handler import GraderBaseHandler
from grader.service.orm.assignment import Assignment
from datetime import datetime
from grader.common.models.error_message import ErrorMessage


def test_string_serialization():
    assert GraderBaseHandler._serialize("test") == "test"


def test_number_serialization():
    assert GraderBaseHandler._serialize(1) == 1
    assert GraderBaseHandler._serialize(2.5) == 2.5


def test_list_serialization():
    assert GraderBaseHandler._serialize([1, 2, 3]) == [1, 2, 3]


def test_tuple_serialization():
    assert GraderBaseHandler._serialize((1, 2, 3)) == (1, 2, 3)


def test_dict_serialization():
    d = {"a": 1, "b": "test", 5: 6}
    s = GraderBaseHandler._serialize(d)
    assert d == s


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
        path="",
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
