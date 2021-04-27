from grader.common.registry import HandlerPathRegistry
import os
import asyncio
import signal
import tornado
from tornado import web
from traitlets import config

# run __init__.py to register handlers
import grader.service
from traitlets.traitlets import Enum, Int, Unicode

class GraderApp(web.Application, config.Application, config.LoggingConfigurable):
  # As an unmanage jupyter hub service, the application gets these environment variables from the hub
  # see: https://jupyterhub.readthedocs.io/en/stable/reference/services.html#launching-a-hub-managed-service
  hub_service_name = Unicode(os.environ.get("JUPYTERHUB_SERVICE_NAME")).tag(config=True)
  hub_api_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN")).tag(config=True)
  hub_api_url = Unicode(os.environ.get("JUPYTERHUB_API_URL")).tag(config=True)
  hub_base_url = Unicode(os.environ.get("JUPYTERHUB_BASE_URL")).tag(config=True)
  hub_service_prefix = Unicode(os.environ.get("JUPYTERHUB_SERVICE_PREFIX")).tag(config=True)
  hub_service_url = Unicode(os.environ.get("JUPYTERHUB_SERVICE_URL")).tag(config=True)

  service_host = Unicode("0.0.0.0", help="The host address of the service").tag(config=True)
  service_port = Int(4010, help="The port the service runs on").tag(config=True)

  log_level = Enum(["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"], "INFO").tag(config=True)


  async def initialize(self, *args, **kwargs):
    self.log.setLevel(self.log_level)
    self.log.info("Starting Initialization...")
    self._start_future = asyncio.Future()
  
  async def cleanup(self):
    pass

  async def start(self):
    self.log.info("Starting Grader Service...")
    self.io_loop = tornado.ioloop.IOLoop.current()

    handlers = HandlerPathRegistry.handler_list()

    # start the webserver
    self.http_server = tornado.httpserver.HTTPServer(
        GraderApp(handlers=handlers),
        # ssl_options=ssl_context,
        xheaders=True,
    )

    self.http_server.listen(self.service_port, address=self.service_host)

    for s in (signal.SIGTERM, signal.SIGINT):
      asyncio.get_event_loop().add_signal_handler(
          s, lambda s=s: asyncio.ensure_future(self.shutdown_cancel_tasks(s))
      )
    
    self.log.info(f"Grader service running at {self.service_host}:{self.service_port}")

    # finish start
    self._start_future.set_result(None)
  
  async def shutdown_cancel_tasks(self, sig):
    """Cancel all other tasks of the event loop and initiate cleanup"""
    self.log.critical("Received signal %s, initiating shutdown...", sig.name)

    # For compatibility with python versions 3.6 or earlier.
    # asyncio.Task.all_tasks() is fully moved to asyncio.all_tasks() starting with 3.9. Also applies to current_task.
    try:
      asyncio_all_tasks = asyncio.all_tasks
      asyncio_current_task = asyncio.current_task
    except AttributeError as e:
      asyncio_all_tasks = asyncio.Task.all_tasks
      asyncio_current_task = asyncio.Task.current_task
        
    tasks = [t for t in asyncio_all_tasks() if t is not asyncio_current_task()]

    if tasks:
        self.log.debug("Cancelling pending tasks")
        [t.cancel() for t in tasks]

        try:
            await asyncio.wait(tasks)
        except asyncio.CancelledError as e:
            self.log.debug("Caught Task CancelledError. Ignoring")
        except StopAsyncIteration as e:
            self.log.error("Caught StopAsyncIteration Exception", exc_info=True)

        tasks = [t for t in asyncio_all_tasks()]
        for t in tasks:
            self.log.debug("Task status: %s", t)
    await self.cleanup()
    asyncio.get_event_loop().stop()

  async def launch_instance_async(self, argv=None):
    try:
        await self.initialize(argv)
        await self.start()
    except Exception as e:
        self.log.exception("")
        self.exit(1)

  @classmethod
  def launch_instance(cls, argv=None):
    self = cls.instance()
    loop = tornado.ioloop.IOLoop.current()
    task = asyncio.ensure_future(self.launch_instance_async(argv))
    try:
        loop.start()
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        if task.done():
            # re-raise exceptions in launch_instance_async
            task.result()
        loop.stop()
  

if __name__ == "__main__":
  GraderApp.launch_instance()