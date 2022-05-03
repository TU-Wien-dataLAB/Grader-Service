# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from nbconvert.preprocessors import ClearOutputPreprocessor

from grader_convert.preprocessors.base import NbGraderPreprocessor


class ClearOutput(NbGraderPreprocessor, ClearOutputPreprocessor):
    pass
