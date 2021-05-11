import os
import pytest
import alembic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from alembic.config import Config
from alembic.command import downgrade, upgrade
from unittest.mock import MagicMock
from grader.service.persistence.database import DataBaseManager



@pytest.fixture
def session():
    cfg = Config(os.path.abspath(os.path.dirname(__file__) + "../../../alembic_test.ini"))
    # cfg.set_main_option('script_location', os.path.abspath(os.path.dirname(__file__) + "../../../alembic"))
    # cfg.set_main_option('sqlalchemy.url', 'sqlite:///:memory:')
    engine = create_engine("sqlite:///:memory:", echo=True)

    with engine.begin() as connection:
      cfg.attributes['connection'] = connection
      # downgrade(cfg, "base")
      upgrade(cfg, "head")

    yield Session(bind=engine)
    engine.dispose()


def insert_users(session):
  session.execute('INSERT INTO "user" ("name") VALUES ("user1")')
  session.execute('INSERT INTO "user" ("name") VALUES ("user2")')
  session.execute('INSERT INTO "user" ("name") VALUES ("user3")')
  session.execute('INSERT INTO "user" ("name") VALUES ("user4")')


def insert_lectures(session):
  session.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture1","WS21","AU.294",false)')
  session.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture2","WS20","AU.297",true)')
  session.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture3","SS22","AU.212",false)')
  session.execute('INSERT INTO "lecture" ("name","semester","code", "complete") VALUES ("lecture4","SS21","AU.194",false)')
  session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",1,"student")')
  session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",2,"student")')
  session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",1,"student")')
  session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",2,"student")')


def insert_assignments(session):
  session.execute('INSERT INTO "assignment" ("name","lectid","duedate","points","status") VALUES ("assignment_1",1,"2021-06-06 23:59:00.000",20,"created")')
  session.execute('INSERT INTO "assignment" ("name","lectid","duedate","points","status") VALUES ("assignment_2",1,"2021-07-07 23:59:00.000",10,"created")')

  session.execute('INSERT INTO "submission" ("date","status","assignid","username") VALUES ("2021-05-05 14:43:35.863","not_graded",1,"user1")')
  session.execute('INSERT INTO "submission" ("date","status","assignid","username") VALUES ("2021-05-07 14:44:35.863","manually_graded",1,"user1")')

  session.execute('INSERT INTO "file" ("name","assignid","path","exercise","points") VALUES ("exercise1.ipynb",1,"./exercise1.ipynb",true,5)')
  session.execute('INSERT INTO "file" ("name","assignid","path","exercise") VALUES ("dataset.csv",1,"./dataset.csv",false)')


def insert_grading(session):
  pass

@pytest.fixture
def user_db(session): # 2
  insert_users(session=session)
  yield session
  session.close()


@pytest.fixture
def lecture_db(session):
  insert_users(session=session)
  insert_lectures(session=session)
  yield session
  session.close()


@pytest.fixture
def full_db(session):
  insert_users(session=session)
  insert_lectures(session=session)
  insert_assignments(session=session)
  insert_grading(session=session)
  yield session
  session.close()

def setup_db_manager_mock(test_session):
    real = DataBaseManager.instance
    m = MagicMock()
    m().create_session.return_value = test_session
    DataBaseManager.instance = m

    def revert():
      DataBaseManager.instance = real
    return revert
