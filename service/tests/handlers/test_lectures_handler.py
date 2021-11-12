import pytest
from server import GraderServer
import json
from api.models.lecture import Lecture
from tornado.httpclient import HTTPClientError

## Imports are important otherwise they will not be found
from .tornado_test_utils import *

@pytest.mark.gen_test
def test_get_lectures(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_url + "/lectures"
    response = yield http_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    lectures = json.loads(response.body.decode())
    assert isinstance(lectures, list)
    assert len(lectures) > 0
    [Lecture.from_dict(l) for l in lectures]  # assert no errors


@pytest.mark.gen_test
def test_post_lectures(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    default_user["groups"] = ["pt__instructor"] # user has to already be in group (we only activate on post)
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = service_url + "/lectures"
    get_response = yield http_client.fetch(
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
    post_response = yield http_client.fetch(
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

    get_response = yield http_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert get_response.code == 200
    lectures = json.loads(get_response.body.decode())
    assert len(lectures) == orig_len + 1


@pytest.mark.gen_test
def test_post_not_found(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures"
    # same code not in user groups
    pre_lecture = Lecture(
        id=-1, name="pytest_lecture", code="pt", complete=False, semester=None
    )
    with pytest.raises(HTTPClientError) as exc_info:
        yield http_client.fetch(
            url,
            method="POST",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(pre_lecture.to_dict()),
        )
    e = exc_info.value
    assert e.code == 404

@pytest.mark.gen_test
def test_get_lecture(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/1"

    get_response = yield http_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    Lecture.from_dict(json.loads(get_response.body.decode()))


@pytest.mark.gen_test
def test_get_lecture_not_found(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/999"

    with pytest.raises(HTTPClientError) as exc_info:
        yield http_client.fetch(
            url,
            method="GET",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 403


@pytest.mark.gen_test
def test_put_lecture(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/3"

    get_response = yield http_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    lecture = Lecture.from_dict(json.loads(get_response.body.decode()))
    lecture.name = "new name"

    put_response = yield http_client.fetch(
        url,
        method="PUT",
        headers={"Authorization": f"Token {default_token}"},
        body=json.dumps(lecture.to_dict()),
    )
    
    assert put_response.code == 200
    put_lecture = Lecture.from_dict(json.loads(put_response.body.decode()))
    assert put_lecture.name == lecture.name


@pytest.mark.gen_test
def test_put_lecture_unauthorized(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/1"

    get_response = yield http_client.fetch(
        url,
        method="GET",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert get_response.code == 200
    lecture = Lecture.from_dict(json.loads(get_response.body.decode()))
    lecture.name = "new name"

    with pytest.raises(HTTPClientError) as exc_info:
        yield http_client.fetch(
            url,
            method="PUT",
            headers={"Authorization": f"Token {default_token}"},
            body=json.dumps(lecture.to_dict()),
        )
    
    e = exc_info.value
    assert e.code == 403


@pytest.mark.gen_test
def test_delete_lecture(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/3"

    delete_response = yield http_client.fetch(
        url,
        method="DELETE",
        headers={"Authorization": f"Token {default_token}"},
    )
    assert delete_response.code == 200

    with pytest.raises(HTTPClientError) as exc_info:
        yield http_client.fetch(
            url,
            method="GET",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 404

@pytest.mark.gen_test
def test_delete_lecture_unauthorized(
    app: GraderServer,
    service_url,
    http_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]
    url = service_url + "/lectures/1"

    with pytest.raises(HTTPClientError) as exc_info:
        yield http_client.fetch(
            url,
            method="DELETE",
            headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 403