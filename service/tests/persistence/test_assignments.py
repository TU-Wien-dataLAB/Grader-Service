from grader.common.models.assignment import Assignment
from grader.common.models.user import User
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .db_util import *
from grader.service.persistence.database import DataBaseManager
from grader.service.persistence import assignment


def test_getassignments(full_db):
    setup_db_manager_mock(full_db)

    assign = assignment.get_assignments(1)
    print(assign)
    assert len(assign) > 0

