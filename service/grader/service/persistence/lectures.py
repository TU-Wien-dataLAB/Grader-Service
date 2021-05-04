from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.common.models.user import User
from grader.common.models.lecture import Lecture
from grader.service.persistence.database import DataBaseManager
import json

def get_lectures(user: User):
    session = DataBaseManager.create_session()
    data =  dict(name=user.name)
    select = 'SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username = :name'
    res = session.execute(text(select), data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def get_lecture(user: User, lectid: int):
    session = DataBaseManager.create_session()
    select = 'SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username= :name AND lecture.id=:id'
    data = dict(name=user.name, id=lectid)
    res = session.execute(select,data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def create_lecture(user: User, lecture: Lecture):
    session = DataBaseManager.create_session()
    insert = 'INSERT INTO "lecture" ("name","semester","code") VALUES (":name",":semester",":code")'
    data = dict(name=lecture.name,semester=lecture.semester,code=lecture.code) 
    session.execute(insert,data)

    select = 'SELECT id FROM lecture WHERE lecture.name=":name"'
    data = dict(name=lecture.name)
    select = session.execute(select,data)
    id = [r[0] for r in select]

    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES (":name",:id,":role")' 
    data = dict(name=user.name, id=id[0],role="instructor")
    session.execute(insert, data)
    session.commit()

def takepart_as_student(user: User, lectid: int):
    session = DataBaseManager.create_session()
    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES (":name",:id,":role")'
    data = dict(name=user.name, id=lectid, role="student")
    session.execute(insert,data)
    session.commit()


def takepart_as_instructor(user: User, lectid: int):
    session = DataBaseManager.create_session()
    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES (":name", :id,":role")'
    data = dict(name=user.name, id=lectid, role="instructor")
    session.execute(insert,data)
    session.commit()

def update_lecture(lecture: Lecture):
    session = DataBaseManager.create_session()
    update = 'UPDATE "lecture" SET name=:name, code=:code, complete=:complete, semester=:semester WHERE id=:id'
    data = dict(name=lecture.name, code=lecture.code, complete=lecture.complete, semster=lecture.semester, id=lecture.id)
    session.execute(update,data)
    session.commit()

def delete_lecture(lectid: int):
    session = DataBaseManager.create_session()
    delete = 'DELETE FROM "lecture" WHERE id=:id'
    data = dict(id=lectid)
    session.execute(delete,data)
    session.commit()
