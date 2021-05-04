from grader.service.persistence.database import DataBaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def get_assignments(lectid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM assignment WHERE lectid=:id ORDER BY duedate ASC")
    select = select.bindparams(id=lectid)
    res = session.execute(select)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM assignment WHERE lectid=:lectid AND id=:id")
    select = select.bindparams(lectid=lectid,id=assignid)
    res = session.execute(select)
    res = json.dumps( [dict(ix) for ix in res] )
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
