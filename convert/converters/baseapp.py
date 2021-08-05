from jupyter_core.application import JupyterApp
from traitlets.traitlets import Enum, Int, TraitError, Unicode, observe, validate
import os

base_converter_aliases = {
    'log-level' : 'Application.log_level',
    'i': 'ConverterApp.input_directory',
    'o': 'ConverterApp.output_directory',
    'p': 'ConverterApp.file_pattern',
    'input_directory': 'ConverterApp.input_directory',
    'output_directory': 'ConverterApp.output_directory',
    'file_pattern': 'ConverterApp.file_pattern',
}
base_converter_flags = {
    'debug': (
        {'Application' : {'log_level' : 'DEBUG'}},
        "set log level to DEBUG (maximize logging output)"
    ),
    'quiet': (
        {'Application' : {'log_level' : 'CRITICAL'}},
        "set log level to CRITICAL (minimize logging output)"
    ),
}

class ConverterApp(JupyterApp):
    description = """Base app for converters
    """

    aliases = base_converter_aliases
    flags = base_converter_flags

    input_directory = Unicode(None, allow_none=False).tag(config=True)
    output_directory = Unicode(None, allow_none=False).tag(config=True)
    file_pattern = Unicode("*.ipynb", allow_none=False).tag(config=True)

    @validate("input_directory", "output_directory")
    def _dir_exits(path: str) -> bool:
        if os.path.exists(path):
            return path
        else:
            return None
