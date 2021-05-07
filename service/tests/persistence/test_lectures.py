from grader.common.models.lecture import Lecture
from grader.common.models.user import User
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import Session
from .db_util import *
from grader.service.persistence.database import DataBaseManager
from grader.service.persistence import lectures
from grader.service import orm


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

  with pytest.raises(sqlalchemy.exc.NoResultFound):
    lectures.get_lecture(User("user1"), lectid=999)


def test_create_lecture(lecture_db):
  setup_db_manager_mock(lecture_db)

  ls = lecture_db.query(orm.Lecture).all()
  num_lects = len(ls)
  test_lecture: Lecture = Lecture(name="Test", code="t", complete=True, semester="20")
  created_lecture = lectures.create_lecture(test_lecture)

  assert created_lecture.name == test_lecture.name
  assert created_lecture.code == test_lecture.code
  assert created_lecture.complete == test_lecture.complete
  assert created_lecture.semester == test_lecture.semester

  ls = lecture_db.query(orm.Lecture).all()
  new_num_lects = len(ls)

  assert num_lects + 1 == new_num_lects

def test_add_user_to_lecture(lecture_db):
  setup_db_manager_mock(lecture_db)

  r = lecture_db.query(orm.Role).filter(orm.Role.lectid == 3 and orm.Role.username == "user1").all()
  assert len(r) == 0

  lectures.add_user_to_lecture(User("user1"), Lecture(id=3), "student")
  r = lecture_db.query(orm.Role).filter(orm.Role.lectid == 3 and orm.Role.username == "user1").all()
  assert len(r) == 1


def test_add_user_to_lecture_unknown_user(lecture_db):
  setup_db_manager_mock(lecture_db)

  r = lecture_db.query(orm.Role).filter(orm.Role.lectid == 3 and orm.Role.username == "test_user").all()
  assert len(r) == 0

  lectures.add_user_to_lecture(User("test_user"), Lecture(id=3), "student")
  r = lecture_db.query(orm.Role).filter(orm.Role.lectid == 3 and orm.Role.username == "test_user").all()
  assert len(r) == 1


def test_update_lecture(lecture_db):
  setup_db_manager_mock(lecture_db)

  l: Lecture = lectures.get_lecture(User("user1"), 1)
  l.name = "new_lecture_name"

  updated_lecture = lectures.update_lecture(l)
  assert updated_lecture.name == "new_lecture_name"

  assert lectures.get_lecture(User("user1"), 1).name == "new_lecture_name"

def test_delete_lecture(lecture_db):
  setup_db_manager_mock(lecture_db)

  lectures.delete_lecture(2)
  with pytest.raises(sqlalchemy.exc.NoResultFound):
    lectures.get_lecture(User("user1"), 2)
