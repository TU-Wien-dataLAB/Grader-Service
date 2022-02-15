import os
from alembic import autogenerate
import pytest
import alembic
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from alembic.config import Config
from alembic.command import downgrade, upgrade, autogen
from unittest.mock import MagicMock
import secrets
from datetime import datetime


def insert_users(session):
    session.execute('INSERT INTO "user" ("name") VALUES ("user1")')
    session.execute('INSERT INTO "user" ("name") VALUES ("user2")')
    session.execute('INSERT INTO "user" ("name") VALUES ("user3")')
    session.execute('INSERT INTO "user" ("name") VALUES ("user4")')


def insert_lectures(session):
    session.execute(
        'INSERT INTO "lecture" ("name","semester","code", "state") VALUES ("lecture1","WS21","AU.294","active")')
    session.execute(
        'INSERT INTO "lecture" ("name","semester","code", "state") VALUES ("lecture1","SS21","AU.294","active")')
    session.execute(
        'INSERT INTO "lecture" ("name","semester","code", "state") VALUES ("lecture2","WS20","AU.297","active")')
    session.execute(
        'INSERT INTO "lecture" ("name","semester","code", "state") VALUES ("lecture3","SS22","AU.212","active")')
    session.execute(
        'INSERT INTO "lecture" ("name","semester","code", "state") VALUES ("lecture4","SS21","AU.194","active")')
    session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",1,"student")')
    session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user1",2,"student")')
    session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",1,"student")')
    session.execute('INSERT INTO "takepart" ("username","lectid","role") VALUES ("user2",2,"student")')


def insert_assignments(ex, lecture_id=1):
    ex.execute(
        f'INSERT INTO "assignment" ("name","lectid","duedate","points","status") VALUES ("assignment_1",{lecture_id},"2021-06-06 23:59:00.000",20,"released")')
    ex.execute(
        f'INSERT INTO "assignment" ("name","lectid","duedate","points","status") VALUES ("assignment_2",{lecture_id},"2021-07-07 23:59:00.000",10,"created")')
    num_inserts = 2
    return num_inserts


def insert_submission(ex, assignment_id=1, username="ubuntu"):
    ex.execute(
        f'INSERT INTO "submission" ("date","auto_status","manual_status","assignid","username","commit_hash","feedback_available") VALUES ("{datetime.now().isoformat(" ", "milliseconds")}","not_graded","not_graded",{assignment_id},"{username}", "{secrets.token_hex(20)}",0)')


def insert_take_part(ex, lecture_id, username="ubuntu", role="student"):
    ex.execute(f'INSERT INTO "takepart" ("username","lectid","role") VALUES ("{username}",{lecture_id},"{role}")')


def insert_grading(session):
    pass

