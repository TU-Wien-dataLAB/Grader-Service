
import json
from pathlib import Path

from ._version import __version__

HERE = Path(__file__).parent.resolve()


import sys
import os.path as path
common_path = path.abspath(path.join(path.dirname(__file__), "../.."))
sys.path.append(common_path)


with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

# import handlers so they get registered
import grading_labextension.handlers

from common.registry import HandlerPathRegistry

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    handlers = HandlerPathRegistry.handler_list(base_url)
    web_app.add_handlers(host_pattern, handlers)


def _jupyter_server_extension_points():
    return [{
        "module": "grading_labextension"
    }]


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    setup_handlers(server_app.web_app)
    server_app.log.info("Registered grader extension at URL path /grading_labextension")

