import pytest
from service.server import GraderServer
import json
from service.api.models.assignment import Assignment
from tornado.httpclient import HTTPClientError
from .db_util import insert_submission

# Imports are important otherwise they will not be found
from .tornado_test_utils import *


async def test_get_assignments(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/1/assignments/"

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    assignments = json.loads(response.body.decode())
    assert isinstance(assignments, list)
    assert len(assignments) > 0
    [Assignment.from_dict(l) for l in assignments]  # assert no errors


async def test_post_assignment(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    get_response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert get_response.code == 200
    assignments = json.loads(get_response.body.decode())
    assert isinstance(assignments, list)
    orig_len = len(assignments)

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))
    assert post_assignment.id != pre_assignment.id
    assert post_assignment.name == pre_assignment.name
    assert post_assignment.type == pre_assignment.type
    assert post_assignment.status == pre_assignment.status
    assert post_assignment.due_date is None
    assert post_assignment.points == 0.0

    get_response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert get_response.code == 200
    assignments = json.loads(get_response.body.decode())
    assert len(assignments) == orig_len + 1


async def test_post_no_status_error(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status=None, points=None)
    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="POST",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(pre_assignment.to_dict()),
        )
    e = exc_info.value
    assert e.code == 400


async def test_put_assignment(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    post_assignment.name = "new name"
    post_assignment.type = "group"
    post_assignment.status = "released"

    url = url + str(post_assignment.id)

    put_response = await http_server_client.fetch(
        url,
        method="PUT",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(post_assignment.to_dict()),
    )
    assert put_response.code == 200
    put_assignment = Assignment.from_dict(json.loads(put_response.body.decode()))
    assert put_assignment.id == post_assignment.id
    assert put_assignment.name == "new name"
    assert put_assignment.type == "group"
    assert put_assignment.status == "released"


async def test_put_assignment_no_point_changes(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    post_assignment.name = "new name"
    post_assignment.type = "group"
    post_assignment.status = "released"
    post_assignment.points = 10.0  # this has no effect

    url = url + str(post_assignment.id)

    put_response = await http_server_client.fetch(
        url,
        method="PUT",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(post_assignment.to_dict()),
    )
    assert put_response.code == 200
    put_assignment = Assignment.from_dict(json.loads(put_response.body.decode()))
    assert put_assignment.id == post_assignment.id
    assert put_assignment.name == "new name"
    assert put_assignment.type == "group"
    assert put_assignment.status == "released"
    assert put_assignment.points != 10.0


async def test_get_assignment(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    url = url + str(post_assignment.id)

    get_response = await http_server_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    get_assignment = Assignment.from_dict(json.loads(get_response.body.decode()))
    assert get_assignment.id == post_assignment.id
    assert get_assignment.name == post_assignment.name
    assert get_assignment.type == post_assignment.type
    assert get_assignment.status == post_assignment.status
    assert get_assignment.points == post_assignment.points
    assert get_assignment.due_date == post_assignment.due_date


async def test_delete_assignment(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    url = url + str(post_assignment.id)

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


async def test_delete_assignment_not_created(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/999"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 404


async def test_delete_assignment_with_submissions(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
        sql_alchemy_db
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    a_id = 1
    url = service_base_url + f"/lectures/3/assignments/{a_id}"

    engine = sql_alchemy_db.engine
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 404


async def test_delete_assignment_same_name_twice(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    url = url + str(post_assignment.id)

    delete_response = await http_server_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert delete_response.code == 200

    url = service_base_url + "/lectures/3/assignments/"

    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    url = url + str(post_assignment.id)

    delete_response = await http_server_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert delete_response.code == 200


async def test_assignment_properties(
        app: GraderServer,
        service_base_url,
        http_server_client,
        jupyter_hub_mock_server,
        default_user,
        default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_base_url + "/lectures/3/assignments/"

    pre_assignment = Assignment(id=-1, name="pytest", type="user", due_date=None, status="created", points=None)
    post_response = await http_server_client.fetch(
        url,
        method="POST",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(pre_assignment.to_dict()),
    )
    assert post_response.code == 200
    post_assignment = Assignment.from_dict(json.loads(post_response.body.decode()))

    url = service_base_url + f"/lectures/3/assignments/{post_assignment.id}/properties"
    prop = {"test": "property", "value": 2, "bool": True, "null": None}
    put_response = await http_server_client.fetch(
        url,
        method="PUT",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(prop),
    )
    assert put_response.code == 200
    get_response = await http_server_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    assignment_props = json.loads(get_response.body.decode())
    assert assignment_props == prop



