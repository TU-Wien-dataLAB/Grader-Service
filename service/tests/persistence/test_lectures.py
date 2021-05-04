from grader.common.models.lecture import Lecture
from grader.common.models.user import User
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .db_util import *
from grader.service.persistence.database import DataBaseManager
from grader.service.persistence import lectures



def test_get_lectures(lecture_db):
  setup_db_manager_mock(lecture_db)

  l = lectures.get_lectures(User("user1"))
  assert len(l) > 0


def test_get_lecture(lecture_db):
  setup_db_manager_mock(lecture_db)

  l = lectures.get_lecture(User("user1"), lectid=1)
  assert type(l) == Lecture

def test_get_lecture_not_found(lecture_db):
  setup_db_manager_mock(lecture_db)

  l = lectures.get_lecture(User("user1"), lectid=999)
  assert l is None