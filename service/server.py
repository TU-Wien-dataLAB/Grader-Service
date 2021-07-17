import os
from tornado import web
from traitlets import config
from traitlets.traitlets import Enum, Int, Integer, Unicode, validate


class GraderServer(config.Configurable, web.Application):
    # As an unmanage jupyter hub service, the application gets these environment variables from the hub
    # see: https://jupyterhub.readthedocs.io/en/stable/reference/services.html#launching-a-hub-managed-service
    hub_service_name = Unicode(os.environ.get("JUPYTERHUB_SERVICE_NAME", "")).tag(
        config=True
    )
    hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN", "")).tag(config=True)
    hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL", "")).tag(config=True)
    hub_base_url = Unicode(os.environ.get("JUPYTERHUB_BASE_URL", "")).tag(config=True)
    hub_service_prefix = Unicode(os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "")).tag(
        config=True
    )
    hub_service_url = Unicode(os.environ.get("JUPYTERHUB_SERVICE_URL", "")).tag(
        config=True
    )

    max_user_cookie_age_days = Integer(15, help="Time in days until cookie expires.").tag(
        config=True
    )

    max_token_cookie_age_minutes = Integer(10, help="Time in minutes until a token cookie expires.").tag(config=True)

    def __init__(self, grader_service_dir: str, **kwargs):
        super().__init__(**kwargs)
        self.grader_service_dir = grader_service_dir
    
    @property
    def max_token_cookie_age_days(self):
        return self.max_token_cookie_age_minutes / 1440
