# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
from tornado import web
from traitlets import config
from traitlets.traitlets import Integer, Unicode


class GraderServer(config.LoggingConfigurable, web.Application):
    # As an unmanage jupyter hub service, the application gets these environment variables from the hub
    # see: https://jupyterhub.readthedocs.io/en/stable/reference/services.html#launching-a-hub-managed-service
    hub_service_name = Unicode(os.environ.get("JUPYTERHUB_SERVICE_NAME", "")).tag(
        config=True
    )
    hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN"), allow_none=False).tag(config=True)
    hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL"), allow_none=False).tag(config=True)
    hub_base_url = Unicode(os.environ.get("JUPYTERHUB_BASE_URL"), allow_none=False).tag(config=True)
    hub_service_prefix = Unicode(os.environ.get("JUPYTERHUB_SERVICE_PREFIX"), allow_none=False).tag(
        config=True
    )
    hub_service_url = Unicode(os.environ.get("JUPYTERHUB_SERVICE_URL"), allow_none=False).tag(
        config=True
    )

    max_user_cookie_age_days = Integer(
        15, help="Time in days until cookie expires."
    ).tag(config=True)

    max_token_cookie_age_minutes = Integer(
        10, help="Time in minutes until a token cookie expires."
    ).tag(config=True)

    def __init__(self, grader_service_dir: str, base_url: str, **kwargs):
        super().__init__(**kwargs)
        self.grader_service_dir = grader_service_dir
        self.base_url = base_url

        self.log.info(f"hub_service_name - { self.hub_service_name }")
        self.log.info(f"hub_api_token - {self.hub_api_token}")
        self.log.info(f"hub_api_url - {self.hub_api_url}")
        self.log.info(f"hub_base_url - {self.hub_base_url}")

    @property
    def max_token_cookie_age_days(self):
        return self.max_token_cookie_age_minutes / 1440
