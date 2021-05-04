import os
from tornado import web
from traitlets import config
from traitlets.traitlets import Enum, Int, Unicode, validate


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
    hub_service_url = Unicode(os.environ.get("JUPYTERHUB_SERVICE_URL", "")).tag(config=True)

