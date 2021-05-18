
import json
import logging
from pathlib import Path
from grader.common.services.request import RequestService
from jupyter_server.serverapp import ServerApp

from ._version import __version__

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]

from grader.grading_labextension import handlers

from grader.common.registry import HandlerPathRegistry

def setup_handlers(web_app: ServerApp):
    host_pattern = ".*$"
    # RequestService.config = web_app.config
    base_url = web_app.settings["base_url"]
    log = logging.getLogger()
    log.critical("#######################################################################")
    log.critical("base_url: " + base_url)
    handlers = HandlerPathRegistry.handler_list(base_url=base_url + "grading_labextension")
    web_app.add_handlers(host_pattern, handlers)



def _jupyter_server_extension_points():
    return [{
        "module": "grader.grading_labextension"
    }]


def _load_jupyter_server_extension(server_app: ServerApp):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    setup_handlers(server_app.web_app)
    server_app.log.info("Registered grading extension at URL path /grading_labextension")

