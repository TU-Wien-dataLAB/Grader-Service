from typing import List
from grader.common.models.assignment_file import AssignmentFile
from grader.common.models.exercise import Exercise
from grader.service.persistence.database import DataBaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def get_assignments(lectid: int) -> List[Assignment]:
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM assignment WHERE lectid=:id ORDER BY duedate ASC")
    select = select.bindparams(id=lectid)
    res = session.execute(select)
    res = [dict(ix) for ix in res]
    res = [Assignment.from_dict({"id": d["id"], "name": d["name"], "due_date": d["duedate"], "status": d["status"]} for d in res)]
    session.commit()
    return res

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM assignment WHERE lectid=:lectid AND id=:id")
    select = select.bindparams(lectid=lectid,id=assignid)
    res = session.execute(select)
    res = [dict(ix) for ix in res]
    session.commit()
    return res

def create_assignment(assignment: Assignment, lectid: int):
    session = DataBaseManager.instance().create_session()

    insert = text("INSERT INTO 'assignment' ('name','lectid','duedate','path','points','status') VALUES (:name,:id,:date,:path,:points,:status)")
    insert = insert.bindparams(name=assignment.name, id=lectid, date=assignment.due_date, path=assignment.path, points=assignment.points, status=assignment.status) 
    session.execute(insert)
    session.commit()

def update_assignment(assignment: Assignment):
    session = DataBaseManager.instance().create_session()

    update = text("UPDATE 'assignment' SET name=:name, duedate=:date, path=:path, points=:points, status=:status WHERE id=:id")
    update = update.bindparams(name=assignment.name, date=assignment.due_date, path=assignment.path, points=assignment.points, status=assignment.status, id=assignment.id)
    session.execute(update)
    session.commit()

def delete_assignment(assignid: Assignment):
    session = DataBaseManager.instance().create_session()

    delete = text("DELETE FROM 'assignment' WHERE id=:id")
    delete = delete.bindparams(id=assignid)
    session.execute(delete)
    session.commit()


def get_exercises(assignment: Assignment) -> List[Exercise]:
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM 'file' where assignid = :aid AND exercise = true;")
    select = select.bindparams(aid=assignment.id)
    res = session.execute(select)
    res = [dict(ex) for ex in res]
    res = [Exercise.from_dict({"id": d["id"], "a_id": d["assignid"], "name": d["name"], "points": d["points"], "path": d["path"]} for d in res)]
    session.commit()
    return res

def get_files(assignment: Assignment) -> List[AssignmentFile]:
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM 'file' where assignid = :aid AND exercise = false;")
    select = select.bindparams(aid=assignment.id)
    res = session.execute(select)
    res = [dict(ex) for ex in res]
    res = [AssignmentFile.from_dict({"id": d["id"], "a_id": d["assignid"], "name": d["name"], "path": d["path"]} for d in res)]
    session.commit()
    return res
