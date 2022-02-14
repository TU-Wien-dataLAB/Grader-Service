import pytest
from grader_service.server import GraderServer
import json

from grader_service.api.models.assignment import Assignment
from grader_service.api.models.lecture import Lecture
from .db_util import insert_submission
from tornado.httpclient import HTTPClientError

# Imports are important otherwise they will not be found
from .tornado_test_utils import *


async def test_get_lectures(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_base_url + "/lectures"
    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    lectures = json.loads(response.body.decode())
    assert isinstance(lectures, list)
    assert len(lectures) > 0
    [Lecture.from_dict(l) for l in lectures]  # assert no errors


async def test_get_lectures_with_semester(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_base_url + "/lectures"
    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    lectures = json.loads(response.body.decode())
    assert isinstance(lectures, list)
    assert len(lectures) > 0
    all_lectures = len(lectures)
    [Lecture.from_dict(l) for l in lectures]  # assert no errors

    url = service_base_url + "/lectures?semester=WS21"
    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    lectures = json.loads(response.body.decode())
    assert isinstance(lectures, list)
    assert len(lectures) > 0
    assert len(lectures) < all_lectures
    [Lecture.from_dict(l) for l in lectures]  # assert no errors


async def test_get_lectures_with_some_parameter(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_base_url + "/lectures?some_param=WS21"
    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url, method="GET", headers={"Authorization": f"Token {default_token}"}
        )
    e = exc_info.value
    assert e.code == 400


async def test_post_lectures(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    default_user["groups"] = ["pt__instructor"]  # user has to already be in group (we only activate on post)
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_base_url + "/lectures"
    get_response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert get_response.code == 200
    lectures = json.loads(get_response.body.decode())
    assert isinstance(lectures, list)
    assert len(lectures) == 0
    orig_len = len(lectures)

    # same code as in group of user
    pre_lecture = Lecture(
        id=-1, name="pytest_lecture", code="pt", complete=False, semester=None
    )
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_lecture.to_dict()),
    )
    assert post_response.code == 200
    post_lecture = Lecture.from_dict(json.loads(post_response.body.decode()))
    assert post_lecture.id != pre_lecture.id
    assert post_lecture.name == pre_lecture.name
    assert post_lecture.code == pre_lecture.code
    assert not post_lecture.complete
    assert post_lecture.semester is None

    get_response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert get_response.code == 200
    lectures = json.loads(get_response.body.decode())
    assert len(lectures) == orig_len + 1


async def test_post_not_found(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures"
    # same code not in user groups
    pre_lecture = Lecture(
        id=-1, name="pytest_lecture", code="pt", complete=False, semester=None
    )
    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="POST",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(pre_lecture.to_dict()),
        )
    e = exc_info.value
    assert e.code == 404


async def test_post_unknown_parameter(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    default_user["groups"] = ["pt__instructor"]  # user has to already be in group (we only activate on post)
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_base_url + "/lectures?some_param=asdf"
    # same code not in user groups
    pre_lecture = Lecture(
        id=-1, name="pytest_lecture", code="pt", complete=False, semester=None
    )
    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="POST",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(pre_lecture.to_dict()),
        )
    e = exc_info.value
    assert e.code == 400


async def test_put_lecture(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3"

    get_response = await http_server_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    lecture = Lecture.from_dict(json.loads(get_response.body.decode()))
    lecture.name = "new name"
    lecture.complete = not lecture.complete
    lecture.semester = "new"
    # lecture code will not be updated
    lecture.code = "some"

    put_response = await http_server_client.fetch(
        url,
        method="PUT",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(lecture.to_dict()),
    )
    
    assert put_response.code == 200
    put_lecture = Lecture.from_dict(json.loads(put_response.body.decode()))
    assert put_lecture.name == lecture.name
    assert put_lecture.complete == lecture.complete
    assert put_lecture.semester == lecture.semester

    assert put_lecture.code != lecture.code


async def test_put_lecture_unauthorized(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/1"

    get_response = await http_server_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    lecture = Lecture.from_dict(json.loads(get_response.body.decode()))
    lecture.name = "new name"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="PUT",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(lecture.to_dict()),
        )
    
    e = exc_info.value
    assert e.code == 403


async def test_get_lecture(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/1"

    get_response = await http_server_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    Lecture.from_dict(json.loads(get_response.body.decode()))


async def test_get_lecture_not_found(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/999"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="GET",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 403


async def test_delete_lecture(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3"

    delete_response = await http_server_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert delete_response.code == 200

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="GET",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 404


async def test_delete_lecture_unauthorized(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/1"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 403


async def test_delete_lecture_assignment_with_submissions(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
    sql_alchemy_db,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    l_id = 3
    a_id = 2
    url = service_base_url + f"/lectures/{l_id}"

    engine = sql_alchemy_db.engine
    insert_assignments(engine, lecture_id=3)
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 400


async def test_delete_lecture_assignment_released(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
    sql_alchemy_db,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    l_id = 3
    url = service_base_url + f"/lectures/{l_id}"

    engine = sql_alchemy_db.engine
    insert_assignments(engine, lecture_id=3)  # assignment with id 1 is status released

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 400


async def test_delete_lecture_assignment_complete(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
    sql_alchemy_db,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    l_id = 3
    url = service_base_url + f"/lectures/{l_id}/assignments"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="complete", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200

    url = service_base_url + f"/lectures/{l_id}"
    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 400

