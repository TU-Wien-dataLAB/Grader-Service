from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def get_assignments(lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM assignment WHERE lectid=%i ORDER BY duedate ASC" % lectid
    #TODO: make it to assignment
    res = session.execute(select)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM assignment WHERE lectid=%i AND id=%i" 
    data = tuple(lectid,assignid)
    res = session.execute(select,data)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

def create_assignment(assignment: Assignment, lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    insert = 'INSERT INTO "assignment" ("name","lectid","duedate","path","points","status") VALUES ("%s",%i,"%s","%s",%i,"%s")'
    data = tuple(assignment.name, lectid, assignment.due_date, assignment.path, assignment.points, assignment.status) 
    session.execute(insert,data)
    session.commit()

def update_assignment(assignment: Assignment):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    update = 'UPDATE "assignment" SET name=%s, duedate=%s, path=%s, points=%i, status=%i WHERE id=%i' 
    data = tuple(assignment.name, assignment.due_date, assignment.path, assignment.points, assignment.status,assignment.id)
    session.execute(update,data)
    session.commit()

def delete_assignment(assignid: Assignment):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    delete = 'DELETE FROM "assignment" WHERE id=%i'
    data = tuple(assignid)
    session.execute(delete,data)
    session.commit()


