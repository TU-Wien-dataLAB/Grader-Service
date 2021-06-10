import pytest
import os
from grader.common.services.git import GitService

def test_git_init(tmpdir):
    lecture_code = "iv21s"
    assignment_name = "assign_1"
    git_service = GitService(lecture_code, assignment_name)

    home = str(tmpdir)
    assignment_dir = str(tmpdir.mkdir(lecture_code).mkdir(assignment_name))

    git_service.git_root_dir = home
    git_service.path = assignment_dir
    git_service.init()

    assert os.path.exists(os.path.join(assignment_dir, ".git"))

