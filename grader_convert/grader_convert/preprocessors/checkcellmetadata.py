# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import traceback
from typing import Dict, Tuple

from nbformat.notebooknode import NotebookNode

from grader_convert.nbgraderformat import MetadataValidator, ValidationError
from grader_convert.preprocessors.base import NbGraderPreprocessor


class CheckCellMetadata(NbGraderPreprocessor):
    """A preprocessor for checking that grade ids are unique."""

    def preprocess(
        self, nb: NotebookNode, resources: Dict
    ) -> Tuple[NotebookNode, Dict]:
        try:
            MetadataValidator().validate_nb(nb)
        except ValidationError as e:
            self.log.error(traceback.format_exc())
            msg = "Notebook failed to validate: " + e.message
            self.log.error(msg)
            raise ValidationError(msg)

        return nb, resources
