import pytest
from server import GraderServer

## Imports are important otherwise they will not be found
from .tornado_test_utils import *


@pytest.mark.gen_test
def test_version_handler(
    app: GraderServer,
    service_base_url,
    http_client,
    base_url,
    jupyter_hub_mock_server,
    default_user,
    default_token
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")

    url = base_url + service_base_url + "/"
    response = yield http_client.fetch(url, headers={"Authorization": f"Token {default_token}"})
    assert response.code == 200
    assert response.body.decode() == "1.0"


@pytest.mark.gen_test
def test_version_handler_with_specifier(
    app: GraderServer,
    service_base_url,
    http_client,
    base_url,
    jupyter_hub_mock_server,
    default_user,
    default_token
):
    http_server = jupyter_hub_mock_server(default_user, default_token)
    app.hub_api_url = http_server.url_for("")

    url = base_url + service_base_url + "/v1/"
    response = yield http_client.fetch(url, headers={"Authorization": f"Token {default_token}"})
    assert response.code == 200
    assert response.body.decode() == "1.0"