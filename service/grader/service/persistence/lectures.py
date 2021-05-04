from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.common.models.user import User
from grader.common.models.lecture import Lecture
from grader.service.persistence.database import DataBaseManager
import json

def get_lectures(user: User) -> List[Lecture]:
    session = DataBaseManager.instance().create_session()
    select = text("SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username = :name")
    select =  select.bindparams(name=user.name)
    res = session.execute(select)
    res = [Lecture.from_dict(dict(x)) for x in res]
    session.commit()
    return res

def get_lecture(user: User, lectid: int) -> Lecture:
    session = DataBaseManager.instance().create_session()
    select = text("SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username= :name AND lecture.id=:id")
    select = select.bindparams(name=user.name, id=lectid)
    res = session.execute(select)
    try:
        res = [Lecture.from_dict(dict(x)) for x in res][0]
    except IndexError:
        return None
    session.commit()
    return res

def create_lecture(user: User, lecture: Lecture) -> None:
    session = DataBaseManager.instance().create_session()
    insert = text("INSERT INTO 'lecture' ('name','semester','code') VALUES (:name,:semester,:code)")
    insert = insert.bindparams(name=lecture.name,semester=lecture.semester,code=lecture.code) 
    session.execute(insert)

    select = text("SELECT id FROM lecture WHERE lecture.name=:name")
    select = select.bindparams(name=lecture.name)
    select = session.execute(select)
    id = [r[0] for r in select]

    insert = text("INSERT INTO 'takepart' ('username','lectid','role') VALUES (:name,:id,:role)") 
    insert = insert.bindparams(name=user.name, id=id[0],role="instructor")
    session.execute(insert)
    session.commit()

def takepart_as_student(user: User, lectid: int) -> None:
    takepart(user, lectid, "student")

def takepart_as_instructor(user: User, lectid: int) -> None:
    takepart(user, lectid, "instructor")

def takepart(user: User, lectid: int, role: str) -> None:
    session = DataBaseManager.instance().create_session()
    insert = text("INSERT INTO 'takepart' ('username','lectid','role') VALUES (:name, :id, :role)")
    insert = insert.bindparams(name=user.name, id=lectid, role=role)
    session.execute(insert)
    session.commit()

def update_lecture(lecture: Lecture) -> None:
    session = DataBaseManager.instance().create_session()
    update = text("UPDATE 'lecture' SET name=:name, code=:code, complete=:complete, semester=:semester WHERE id=:id")
    update = update.bindparams(name=lecture.name, code=lecture.code, complete=lecture.complete, semster=lecture.semester, id=lecture.id)
    session.execute(update)
    session.commit()

def delete_lecture(lectid: int) -> None:
    session = DataBaseManager.instance().create_session()
    delete = text("DELETE FROM 'lecture' WHERE id=:id")
    delete = delete.bindparams(id=lectid)
    session.execute(delete)
    session.commit()
