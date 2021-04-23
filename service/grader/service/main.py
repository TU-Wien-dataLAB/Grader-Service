from grader.common.registry import HandlerPathRegistry
import os
import tornado
from tornado.web import Application
from traitlets.config import LoggingConfigurable

# run __init__.py to register handlers
import grader.service
from traitlets.traitlets import Unicode

class GraderApp(Application, LoggingConfigurable):
  # As an unmanage jupyter hub service, the application gets these environment variables from the hub
  # see: https://jupyterhub.readthedocs.io/en/stable/reference/services.html#launching-a-hub-managed-service
  hub_service_name = Unicode(os.environ.get("JUPYTERHUB_SERVICE_NAME")).tag(config=True)
  hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN")).tag(config=True)
  hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL")).tag(config=True)
  hub_base_url = Unicode(os.environ.get("JUPYTERHUB_BASE_URL")).tag(config=True)
  hub_service_prefix = Unicode(os.environ.get("JUPYTERHUB_SERVICE_PREFIX")).tag(config=True)
  hub_service_url = Unicode(os.environ.get("JUPYTERHUB_SERVICE_URL")).tag(config=True)
  


def main():
  """
  Runs the GraderExtensionHandler tornado server locally without being attached to a jupyter_server.
  """
  print("Starting Extension handler... ", end="")
  handlers = HandlerPathRegistry.handler_list()
  app = GraderApp(handlers, debug=True)
  print("Done")
  app.listen(4010)
  tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()