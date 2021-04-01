#!/usr/bin/env python3

import connexion
from connexion.mock import MockResolver

# from swagger_server import encoder

# our hardcoded mock "Bearer" access tokens
TOKENS = {
    '123': 'jdoe',
    '456': 'rms'
}


def get_secret(user) -> str:
    return 'You are: {uid}'.format(uid=user)


def token_info(access_token) -> dict:
    uid = TOKENS.get(access_token)
    if not uid:
        return None
    return {'uid': uid, 'scope': 'instructor tutor student'}

def main():
    app = connexion.App(__name__)
    # app.app.json_encoder = encoder.JSONEncoder
    app.add_api('./openapi.yml', resolver=MockResolver(mock_all=True), base_path="/services/mock")
    app.run(port=8000)


if __name__ == '__main__':
    main()
