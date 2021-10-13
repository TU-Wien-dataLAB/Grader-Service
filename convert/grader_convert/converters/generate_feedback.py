import os
from typing import Any

from traitlets.config import Config
from traitlets import List, default
from nbconvert.exporters import HTMLExporter
from nbconvert.preprocessors import CSSHTMLHeaderPreprocessor

from .base import BaseConverter
from ..preprocessors import GetGrades
from ..converters.baseapp import ConverterApp


class GenerateFeedback(BaseConverter):
    preprocessors = List([GetGrades, CSSHTMLHeaderPreprocessor]).tag(config=True)

    @default("classes")
    def _classes_default(self):
        classes = super(GenerateFeedback, self)._classes_default()
        classes.append(HTMLExporter)
        return classes

    @default("export_class")
    def _exporter_class_default(self):
        return HTMLExporter

    @default("permissions")
    def _permissions_default(self):
        return 664

    def __init__(
        self, input_dir: str, output_dir: str, file_pattern: str, **kwargs: Any
    ):
        super(GenerateFeedback, self).__init__(
            input_dir, output_dir, file_pattern, **kwargs
        )
        c = Config()
        if "template_file" not in self.config.HTMLExporter:
            c.HTMLExporter.template_file = "feedback.tpl"
        if "template_path" not in self.config.HTMLExporter:
            template_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "templates",
                )
            )
            c.HTMLExporter.template_path = [".", template_path]
        self.update_config(c)
        self.force = True  # always overwrite generated assignments


class GenerateFeedbackApp(ConverterApp):
    version = ConverterApp.__version__

    def start(self):
        GenerateFeedback(
            input_dir=self.input_directory,
            output_dir=self.output_directory,
            file_pattern=self.file_pattern,
        ).start()