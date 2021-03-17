from jupyter_server.base.handlers import JupyterHandler
import tornado


class GraderExtensionHandler(JupyterHandler):
  pass



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
