# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import asyncio
import logging
import os
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import inspect

import tornado
from tornado.httpserver import HTTPServer
from tornado_sqlalchemy import SQLAlchemy
from traitlets import config, Bool, Type
from traitlets import log as traitlets_log
from traitlets import Enum, Int, TraitError, Unicode, observe, validate, default, HasTraits

# run __init__.py to register handlers
import grader_service.handlers
from grader_service.auth.hub import JupyterHubGroupAuthenticator
from grader_service.autograding.local_grader import LocalAutogradeExecutor
from grader_service.handlers.base_handler import RequestHandlerConfig
from grader_service.registry import HandlerPathRegistry
from grader_service.server import GraderServer
from grader_service.autograding.grader_executor import GraderExecutor
from grader_service._version import __version__


class GraderService(config.Application):
    name = "grader-service"
    version = __version__

    description = """Starts the grader service, which can be used to create and distribute assignments,
  collect submissions and grade them.
  """

    examples = """
  generate default config file:
      grader-service --generate-config -f /etc/grader/grader_service_config.py
  spawn the grader service:
      grader-service -f /etc/grader/grader_service_config.py
  """

    generate_config = Bool(False, help="Generate config file based on defaults.").tag(config=True)

    service_host = Unicode(os.getenv("GRADER_SERVICE_HOST", "0.0.0.0"), help="The host address of the service").tag(
        config=True
    )
    service_port = Int(int(os.getenv("GRADER_SERVICE_PORT", "4010")), help="The port the service runs on").tag(
        config=True)

    reuse_port = Bool(False, help="Whether to allow for the specified service port to be reused.").tag(config=True)

    grader_service_dir = Unicode(os.getenv("GRADER_SERVICE_DIRECTORY"), allow_none=False).tag(config=True)

    db_url = Unicode(allow_none=False).tag(config=True)

    max_body_size = Int(104857600, help="Sets the max buffer size in bytes, default to 100mb").tag(config=True)

    max_buffer_size = Int(104857600, help="Sets the max body size in bytes, default to 100mb").tag(config=True)

    @default('db_url')
    def _default_username(self):
        service_dir_url = f'sqlite:///{os.path.join(self.grader_service_dir, "grader.db")}'
        return os.getenv("GRADER_DB_URL", service_dir_url)

    service_git_username = Unicode("grader-service", allow_none=False).tag(config=True)
    service_git_email = Unicode("", allow_none=False).tag(config=True)

    config_file = Unicode(
        "grader_service_config.py", help="The config file to load"
    ).tag(config=True)

    base_url_path = Unicode("/services/grader", allow_none=False).tag(config=True)

    authenticator_class = Type(default_value=JupyterHubGroupAuthenticator, klass=object, allow_none=False, config=True)

    @validate("config_file")
    def _validate_config_file(self, proposal):
        if not os.path.isfile(proposal.value) and not self.generate_config:
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
        'generate-config': (
            {'GraderService': {'generate_config': True}},
            "generate default config file",
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

    def setup_loggers(self, log_level: str):  # pragma: no cover
        """Handles application, Tornado, and SQLAlchemy logging configuration."""
        stream_handler = logging.StreamHandler
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        fmt = "%(color)s%(levelname)-8s %(asctime)s %(module)-13s |%(end_color)s %(message)s"
        formatter = tornado.log.LogFormatter(fmt=fmt, color=True, datefmt=None)

        for log in ("access", "application", "general"):
            logger = logging.getLogger("tornado.{}".format(log))
            if len(logger.handlers) > 0:
                logger.removeHandler(logger.handlers[0])
            logger.setLevel(log_level)
            handler = stream_handler(stream=sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        sql_logger = logging.getLogger("sqlalchemy")
        sql_logger.propagate = False
        sql_logger.setLevel("WARN")
        sql_handler = stream_handler(stream=sys.stdout)
        sql_handler.setLevel("WARN")
        sql_handler.setFormatter(formatter)
        sql_logger.addHandler(sql_handler)

        traitlet_logger = traitlets_log.get_logger()
        traitlet_logger.removeHandler(traitlet_logger.handlers[0])
        traitlet_logger.setLevel(log_level)
        traitlets_handler = stream_handler(stream=sys.stdout)
        traitlets_handler.setFormatter(formatter)
        traitlet_logger.addHandler(traitlets_handler)

    def write_config_file(self):
        self.log.info(f"Writing config file {os.path.abspath(self.config_file)}")
        config_file_dir = os.path.dirname(os.path.abspath(self.config_file))
        if not os.path.isdir(config_file_dir):
            self.exit(f"The directory to write the config file has to exist. {config_file_dir} not found")
        if os.path.isfile(os.path.abspath(self.config_file)):
            self.exit(f"Config file {os.path.abspath(self.config_file)} already exists!")

        config_classes = [x[1] for x in inspect.getmembers(sys.modules[__name__],
                                                           lambda x: inspect.isclass(x) and issubclass(x, HasTraits))]
        config_text = self.generate_config_file(classes=config_classes)
        if isinstance(config_text, bytes):
            config_text = config_text.decode('utf8')
        print("Generating config: %s" % self.config_file)
        with open(self.config_file, mode='w') as f:
            f.write(config_text)

    def initialize(self, argv, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.setup_loggers(self.log_level)
        self.log.info("Starting Initialization...")
        self._start_future = asyncio.Future()

        if sys.version_info.major < 3 or sys.version_info.minor < 8:
            raise RuntimeError("Grader Service needs Python version 3.8 or above to run!")
        if shutil.which("git") is None:
            raise RuntimeError("No git executable found! Git is necessary to run Grader Service!")

        self.parse_command_line(argv)
        self.log.info("Loading config file...")
        self.load_config_file(self.config_file)

    async def cleanup(self):
        pass

    async def start(self):
        self.log.info(f"Config File: {os.path.abspath(self.config_file)}")

        if self.generate_config:
            self.write_config_file()
            self.exit(0)

        self.log.info("Starting Grader Service...")
        self.io_loop = tornado.ioloop.IOLoop.current()

        await self._setup_environment()

        # pass config to DataBaseManager and GraderExecutor
        GraderExecutor.config = self.config
        RequestHandlerConfig.config = self.config

        handlers = HandlerPathRegistry.handler_list(self.base_url_path)

        isSQLite = 'sqlite://' in self.db_url

        # start the webserver
        self.http_server: HTTPServer = HTTPServer(
            GraderServer(
                grader_service_dir=self.grader_service_dir,
                base_url=self.base_url_path,
                auth_cls=self.authenticator_class,
                handlers=handlers,
                cookie_secret=secrets.token_hex(
                    nbytes=32
                ),  # generate new cookie secret at startup
                config=self.config,
                db=SQLAlchemy(self.db_url, engine_options={} if isSQLite else {"pool_size": 50, "max_overflow": -1}),
                parent=self,
            ),
            # ssl_options=ssl_context,
            max_buffer_size=self.max_buffer_size,
            max_body_size=self.max_body_size,
            xheaders=True,
        )
        self.log.info(f"Service directory - {self.grader_service_dir}")
        self.http_server.bind(self.service_port, address=self.service_host, reuse_port=self.reuse_port)
        self.http_server.start()

        for s in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                s, lambda s=s: asyncio.ensure_future(self.shutdown_cancel_tasks(s))
            )

        self.log.info(
            f"Grader service running at {self.service_host}:{self.service_port}"
        )

        # finish start
        self._start_future.set_result(None)

    async def _setup_environment(self):
        if not os.path.exists(os.path.join(self.grader_service_dir, "git")):
            os.mkdir(os.path.join(self.grader_service_dir, "git"))
        # check if git config exits so that git commits don't fail
        subprocess.run(shlex.split("git config --global init.defaultBranch main"))
        if subprocess.check_output(shlex.split("git config user.name")).decode("utf-8").strip() == "":
            subprocess.run(shlex.split(f'git config --global user.name "{self.service_git_username}"'))
        if subprocess.check_output(shlex.split("git config user.email")).decode("utf-8").strip() == "":
            subprocess.run(shlex.split(f'git config --global user.email "{self.service_git_email}"'))

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
            self.log.exception(e)
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

    @validate("grader_service_dir")
    def _validate_service_dir(self, proposal):
        path: str = proposal["value"]
        if not os.path.isabs(path):
            raise TraitError("The path is not absolute")
        if not os.path.isdir(path):
            os.mkdir(path, mode=0o700)
        return path

    @observe("grader_service_dir")
    def _observe_service_dir(self, change):
        path = change["new"]
        git_path = os.path.join(path, "git")
        if not os.path.isdir(git_path):
            os.mkdir(git_path, mode=0o700)


main = GraderService.launch_instance

if __name__ == "__main__":
    main(sys.argv)
