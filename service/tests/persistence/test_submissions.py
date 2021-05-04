from grader.common.models.user import User
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from .db_util import *
from grader.service.persistence.database import DataBaseManager
from grader.service.persistence import submissions

def test_get_submissions(full_db):
  setup_db_manager_mock(full_db)

  s = submissions.get_submissions(User("user1"), 1, latest=false)
  assert len(s) > 0