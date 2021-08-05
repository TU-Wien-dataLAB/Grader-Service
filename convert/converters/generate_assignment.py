from sys import path
from baseapp import ConverterApp
import os
import re
from textwrap import dedent

from traitlets import List, Bool, default

from base import BaseConverter, GraderConvertException
from ..preprocessors import (
    IncludeHeaderFooter,
    ClearSolutions,
    LockCells,
    ComputeChecksums,
    SaveCells,
    CheckCellMetadata,
    ClearOutput,
    ClearHiddenTests,
    ClearMarkScheme,
)
from traitlets.config.loader import Config
from typing import Any


class GenerateAssignment(BaseConverter):

    create_assignment = Bool(
        True,
        help=dedent(
            """
            Whether to create the assignment at runtime if it does not
            already exist.
            """
        ),
    ).tag(config=True)

    @default("permissions")
    def _permissions_default(self) -> int:
        return 664 if self.coursedir.groupshared else 644

    preprocessors = List(
        [
            IncludeHeaderFooter,
            LockCells,
            ClearSolutions,
            ClearOutput,
            CheckCellMetadata,
            ComputeChecksums,
            SaveCells,
            ClearHiddenTests,
            ClearMarkScheme,
            ComputeChecksums,
            CheckCellMetadata,
        ]
    ).tag(config=True)
    # NB: ClearHiddenTests must come after ComputeChecksums and SaveCells.
    # ComputerChecksums must come again after ClearHiddenTests.

    def _load_config(self, cfg: Config, **kwargs: Any) -> None:
        super(GenerateAssignment, self)._load_config(cfg, **kwargs)

    def __init__(
        self, input_dir: str, output_dir: str, file_pattern: str, **kwargs: Any
    ) -> None:
        super(GenerateAssignment, self).__init__(
            input_dir, output_dir, file_pattern, **kwargs
        )

    def init_assignment(self, assignment_id: str, student_id: str) -> None:
        super(GenerateAssignment, self).init_assignment(assignment_id, student_id)

    def start(self) -> None:
        super(GenerateAssignment, self).start()


class GenerateAssignmentApp(ConverterApp):
    version = ConverterApp.__version__

    def start(self):
        GenerateAssignment(
            input_dir=self.input_directory,
            output_dir=self.output_directory,
            file_pattern=self.file_pattern,
        ).start()

if __name__ == "__main__":
    cfg = {
        "input_directory": "/etc",
        "output_directory": os.path.expanduser("~")
    }
    app = GenerateAssignmentApp()
    app.start()