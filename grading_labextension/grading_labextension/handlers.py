import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class GraderExtensionHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /grading_labextension/get_example endpoint!"
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "grading_labextension", "get_example")
    handlers = [(route_pattern, GraderExtensionHandler)]
    web_app.add_handlers(host_pattern, handlers)


def main():
  """
  Runs the GraderExtensionHandler tornado server locally without being attached to a jupyter_server.
  """
  print("Starting Extension handler... ", end="")
  handlers = [
    ('.*$', GraderExtensionHandler)
  ]
  app = tornado.web.Application(handlers, debug=True)
  print("Done")
  app.listen(8888)
  tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
  main()

