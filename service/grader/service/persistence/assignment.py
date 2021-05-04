from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def get_assignments(lectid: int):
    session = DataBaseManager.create_session()

    select = "SELECT * FROM assignment WHERE lectid=:id ORDER BY duedate ASC"
    data = dict(id=lectid)
    res = session.execute(select, data)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int):
    session = DataBaseManager.create_session()

    select = "SELECT * FROM assignment WHERE lectid=:lectid AND id=:id" 
    data = dict(lectid=lectid,id=assignid)
    res = session.execute(select,data)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

def create_assignment(assignment: Assignment, lectid: int):
    session = DataBaseManager.create_session()

    insert = 'INSERT INTO "assignment" ("name","lectid","duedate","path","points","status") VALUES (":name",:id,":date",":path",:points,":status")'
    data = dict(name=assignment.name, id=lectid, date=assignment.due_date, path=assignment.path, points=assignment.points, status=assignment.status) 
    session.execute(insert,data)
    session.commit()

def update_assignment(assignment: Assignment):
    session = DataBaseManager.create_session()

    update = 'UPDATE "assignment" SET name=":name", duedate=:date, path=":path", points=:points, status=":status" WHERE id=:id' 
    data = dict(name=assignment.name, date=assignment.due_date, path=assignment.path, points=assignment.points, status=assignment.status, id=assignment.id)
    session.execute(update,data)
    session.commit()

def delete_assignment(assignid: Assignment):
    session = DataBaseManager.create_session()

    delete = 'DELETE FROM "assignment" WHERE id=:id'
    data = dict(id=assignid)
    session.execute(delete,data)
    session.commit()


