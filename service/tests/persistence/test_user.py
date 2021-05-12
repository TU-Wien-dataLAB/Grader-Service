from grader.service.orm.user import User
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from .db_util import *
from grader.service.persistence.database import DataBaseManager
from grader.service.persistence import user

def test_create_user(full_db):
  revert = setup_db_manager_mock(full_db)
  user.create_user(User(name="test"))
  assert user.user_exists(User(name="test"))
  revert()
