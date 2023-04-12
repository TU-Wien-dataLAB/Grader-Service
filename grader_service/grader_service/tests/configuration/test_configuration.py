# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import pytest
import os


@pytest.fixture(scope="function")
def tempdirpath(tmpdir):
    config_path = \
        tmpdir.mkdir("grader_service").join("grader_service_config.py")
    with open(config_path, 'w+') as _:
        pass
    yield tmpdir


async def test_wrong_grader_service_config_path(tempdirpath):
    wrong_config_path = tempdirpath.join("grader_service_config.py")
    cmd = f'grader-service -f {wrong_config_path}'
    output = os.system(cmd)
    assert output == 256

