from datetime import datetime
from re import sub
import secrets
import pytest
from service.server import GraderServer
import json
from service.api.models.user import User
from service.api.models.submission import Submission
from tornado.httpclient import HTTPClientError
from datetime import timezone
from .db_util import insert_submission, insert_take_part

# Imports are important otherwise they will not be found
from .tornado_test_utils import *


async def test_get_submissions(
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

    a_id = 1
    url = service_base_url + f"/lectures/1/assignments/{a_id}/submissions/"

    engine = sql_alchemy_db.engine
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    submissions = json.loads(response.body.decode())
    assert isinstance(submissions, list)
    assert len(submissions) == 1
    user_submissions = submissions[0]
    user = User.from_dict(user_submissions["user"])
    assert user.name == default_user["name"]

    submissions_list = user_submissions["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 2
    assert all([isinstance(s, dict) for s in submissions_list])
    [Submission.from_dict(s) for s in submissions_list]


async def test_get_submissions_latest(
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

    a_id = 1
    url = service_base_url + f"/lectures/1/assignments/{a_id}/submissions/?latest=true"

    engine = sql_alchemy_db.engine
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    submissions = json.loads(response.body.decode())
    assert isinstance(submissions, list)
    assert len(submissions) == 1
    user_submissions = submissions[0]
    user = User.from_dict(user_submissions["user"])
    assert user.name == default_user["name"]

    submissions_list = user_submissions["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 1
    assert isinstance(submissions_list[0], dict)
    Submission.from_dict(submissions_list[0])


async def test_get_submissions_instructor_version(
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
    a_id = 3
    engine = sql_alchemy_db.engine
    insert_assignments(engine, l_id)

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/?instructor-version=true"

    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username="user1")
    insert_submission(engine, assignment_id=a_id, username="user1")

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    submissions = json.loads(response.body.decode())
    assert isinstance(submissions, list)
    assert len(submissions) == 2
    # Submissions of first user
    user_submission = submissions[0]

    possible_users = {default_user["name"], "user1"}
    user = User.from_dict(user_submission["user"])
    assert user.name in possible_users
    possible_users.remove(user.name)

    submissions_list = user_submission["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 2
    assert all([isinstance(s, dict) for s in submissions_list])
    [Submission.from_dict(s) for s in submissions_list]

    user_submission = submissions[1]

    user = User.from_dict(user_submission["user"])
    assert user.name in possible_users
    possible_users.remove(user.name)
    assert len(possible_users) == 0

    submissions_list = user_submission["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 2
    assert all([isinstance(s, dict) for s in submissions_list])
    [Submission.from_dict(s) for s in submissions_list]


async def test_get_submissions_instructor_version_unauthorized(
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

    l_id = 1 # default user is student
    a_id = 1
    engine = sql_alchemy_db.engine

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/?instructor-version=true"

    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url, method="GET", headers={"Authorization": f"Token {default_token}"}
        )
    e = exc_info.value
    assert e.code == 403


async def test_get_submissions_latest_instructor_version(
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
    a_id = 3
    engine = sql_alchemy_db.engine
    insert_assignments(engine, l_id)

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/?instructor-version=true&latest=true"

    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username=default_user["name"])
    insert_submission(engine, assignment_id=a_id, username="user1")
    insert_submission(engine, assignment_id=a_id, username="user1")

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"}
    )
    assert response.code == 200
    submissions = json.loads(response.body.decode())
    assert isinstance(submissions, list)
    assert len(submissions) == 2
    # Submissions of first user
    user_submission = submissions[0]

    possible_users = {default_user["name"], "user1"}
    user = User.from_dict(user_submission["user"])
    assert user.name in possible_users
    possible_users.remove(user.name)

    submissions_list = user_submission["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 1
    assert all([isinstance(s, dict) for s in submissions_list])
    [Submission.from_dict(s) for s in submissions_list]

    user_submission = submissions[1]

    user = User.from_dict(user_submission["user"])
    assert user.name in possible_users
    possible_users.remove(user.name)
    assert len(possible_users) == 0

    submissions_list = user_submission["submissions"]
    assert isinstance(submissions_list, list)
    assert len(submissions_list) == 1
    assert all([isinstance(s, dict) for s in submissions_list])
    [Submission.from_dict(s) for s in submissions_list]


async def test_get_submission(
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

    l_id = 3 # user has to be instructor
    a_id = 3
    engine = sql_alchemy_db.engine
    insert_assignments(engine, l_id)

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/1/"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url, method="GET", headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 404

    insert_submission(engine, a_id, default_user["name"])

    response = await http_server_client.fetch(
        url, method="GET", headers={"Authorization": f"Token {default_token}"},
    )
    assert response.code == 200
    submission_dict = json.loads(response.body.decode())
    Submission.from_dict(submission_dict)


async def test_get_submission_unauthorized(
    app: GraderServer,
    service_base_url,
    http_server_client,
    jupyter_hub_mock_server,
    default_user,
    default_token,
):  
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")[0:-1]

    l_id = 1 # user is student
    a_id = 1

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/1/"

    with pytest.raises(HTTPClientError) as exc_info:
        await http_server_client.fetch(
            url, method="GET", headers={"Authorization": f"Token {default_token}"},
        )
    e = exc_info.value
    assert e.code == 403


async def test_put_submission(
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

    l_id = 3 # default user is student
    a_id = 3

    url = service_base_url + f"/lectures/{l_id}/assignments/{a_id}/submissions/1/"

    engine = sql_alchemy_db.engine
    insert_assignments(engine, l_id)
    insert_submission(engine, a_id, default_user["name"])

    now = datetime.utcnow().isoformat("T", "milliseconds") + "Z"
    pre_submission = Submission(id=-1, submitted_at=now, commit_hash=secrets.token_hex(20), auto_status="automatically_graded", manual_status="manually_graded")
    response = await http_server_client.fetch(
        url, method="PUT", headers={"Authorization": f"Token {default_token}"}, body=json.dumps(pre_submission.to_dict()),
    )
    assert response.code == 200
    submission_dict = json.loads(response.body.decode())
    submission = Submission.from_dict(submission_dict)
    assert submission.id == 1
    assert submission.auto_status == pre_submission.auto_status
    assert submission.manual_status == pre_submission.manual_status
    assert submission.commit_hash != pre_submission.commit_hash # commit hash cannot be changed
    assert not submission.feedback_available
    assert submission.submitted_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3] + "Z" == pre_submission.submitted_at
    assert submission.score is None


