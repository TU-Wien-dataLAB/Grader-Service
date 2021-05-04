import logging
import sys
from grader.common.registry import HandlerPathRegistry
import os
import asyncio
import signal
import tornado
from tornado import web
from tornado.httpserver import HTTPServer
from traitlets import config

# run __init__.py to register handlers
import grader.service
from traitlets.traitlets import Enum, Int, Unicode, validate
from grader.service.server import GraderServer


class GraderService(config.Application):

    name = "grader-service"
    version = "0.1.0"

    description = """Starts the grader service, which can be used to create and distribute assignments,
  collect submissions and grade them.
  """

    examples = """
  generate default config file:
      grader-service --generate-config -f /etc/grader/grader_service_config.py
  spawn the grader service:
      grader-service -f /etc/grader/grader_service_config.py
  """

    service_host = Unicode("0.0.0.0", help="The host address of the service").tag(
        config=True
    )
    service_port = Int(4010, help="The port the service runs on").tag(config=True)

    config_file = Unicode(
        "grader_service_config.py", help="The config file to load"
    ).tag(config=True)

    @validate("config_file")
    def _validate_config_file(self, proposal):
        if not os.path.isfile(proposal.value):
            print(
                "ERROR: Failed to find specified config file: {}".format(
                    proposal.value
                ),
                file=sys.stderr,
            )
            sys.exit(1)
        return proposal.value

    flags = {
        "debug": (
            {
                "Application": {
                    "log_level": logging.DEBUG,
                },
            },
            "Set log-level to debug, for the most verbose logging.",
        ),
        "show-config": (
            {
                "Application": {
                    "show_config": True,
                },
            },
            "Show the application's configuration (human-readable format)",
        ),
        "show-config-json": (
            {
                "Application": {
                    "show_config_json": True,
                },
            },
            "Show the application's configuration (json format)",
        ),
    }

    aliases = {
        "log-level": "Application.log_level",
        "f": "GraderService.config_file",
        "config": "GraderService.config_file",
    }

    log_level = Enum(
        ["CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"],
        "INFO",
    ).tag(config=True)

    def initialize(self, argv, *args, **kwargs):
        super().initialize(*args, **kwargs)
        logging.basicConfig(format=f"%(color)s[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s %(module)s:%")
        self.log.setLevel(self.log_level)
        self.log.info("Starting Initialization...")
        self._start_future = asyncio.Future()

        self.parse_command_line(argv)
        self.load_config_file(self.config_file)

    async def cleanup(self):
        pass

    async def start(self):
        self.log.info("Starting Grader Service...")
        self.io_loop = tornado.ioloop.IOLoop.current()

        handlers = HandlerPathRegistry.handler_list()

        # start the webserver
        self.http_server: HTTPServer = HTTPServer(
            GraderServer(handlers=handlers, config=self.config),
            # ssl_options=ssl_context,
            xheaders=True,
        )

        self.http_server.listen(self.service_port, address=self.service_host)

        for s in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                s, lambda s=s: asyncio.ensure_future(self.shutdown_cancel_tasks(s))
            )

        self.log.info(
            f"Grader service running at {self.service_host}:{self.service_port}"
        )

        self.log.info(f"GraderServer: hub_service_name - { self.http_server.request_callback.hub_service_name }")
        self.log.info(f"GraderServer: hub_api_token - {self.http_server.request_callback.hub_api_token}")
        self.log.info(f"GraderServer: hub_api_url - {self.http_server.request_callback.hub_api_url}")
        self.log.info(f"GraderServer: hub_base_url - {self.http_server.request_callback.hub_base_url}")

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
            self.initialize(argv)
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


main = GraderService.launch_instance

if __name__ == "__main__":
    main(sys.argv)
