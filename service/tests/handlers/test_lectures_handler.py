import pytest
from server import GraderServer
import json
from api.models.lecture import Lecture

## Imports are important otherwise they will not be found
from .tornado_test_utils import *


@pytest.mark.gen_test
def test_get_lectures(
    app: GraderServer,
    service_base_url,
    http_client,
    base_url,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")

    url = base_url + service_base_url + "/lectures"
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
    service_base_url,
    http_client,
    base_url,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):
    default_user["groups"] = ["pt__instructor"] # user has to already be in group (we only activate on post)
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    url = base_url + service_base_url + "/lectures"
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
