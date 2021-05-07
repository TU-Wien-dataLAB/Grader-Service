from typing import List
from grader.common.models.assignment_file import AssignmentFile
from grader.common.models.exercise import Exercise
from grader.service.persistence.database import DataBaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.service import orm
from grader.common.models.assignment import Assignment
import json

def get_assignments(lectid: int) -> List[Assignment]:
    session = DataBaseManager.instance().create_session()

    select = session.query(orm.Assignment).filter(orm.Assignment.lectid == lectid).all()
    res = []
    for a in select:
        a_model = Assignment()
        a_model.id = a.id
        a_model.name = a.name
        a_model.due_date = a.duedate
        a_model.status = a.status
        a_model.exercises = [AssignmentFile(name=f.name, hashcode=None, path=f.path) for f in a.files if f.exercise]
        a_model.files = [AssignmentFile(name=f.name, hashcode=None, path=f.path) for f in a.files if not f.exercise]
        res.append(a_model)
    session.commit()
    return res

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int) -> Assignment:
    session = DataBaseManager.instance().create_session()

    a = session.query(orm.Assignment).filter(orm.Assignment.lectid == lectid, orm.Assignment.id == assignid).one()
    a_model = Assignment()
    a_model.id = a.id
    a_model.name = a.name
    a_model.due_date = a.duedate
    a_model.status = a.status
    a_model.exercises = [AssignmentFile(name=f.name, hashcode=None, path=f.path) for f in a.files if f.exercise]
    a_model.files = [AssignmentFile(name=f.name, hashcode=None, path=f.path) for f in a.files if not f.exercise]
    
    session.commit()
    return a_model

def create_assignment(assignment: Assignment, lectid: int):
    session = DataBaseManager.instance().create_session()

    #TODO: points and path not yet set
    assignment = orm.Assignment(name=assignment.name,lectid=lectid, duedate=assignment.due_date, path='', points=0, status=assignment.status)
    session.add(assignment)
    session.commit()

def update_assignment(assignment: Assignment):
    session = DataBaseManager.instance().create_session()

    assign = session.query(orm.Assignment).filter(orm.Assignment.id==assignment.id).one()
    assign.name = assignment.name
    assign.duedate = assignment.due_date
    # assignment model doesnt have a path
    #assign.path = assignment.path
    # also doesnt have points -> not a bad thing just clarification
    #assign.points = assignment.points
    assign.status = assignment.status
    session.commit()

def delete_assignment(assignment: Assignment):
    session = DataBaseManager.instance().create_session()

    assign = session.query(orm.Assignment).filter(orm.Assignment.id==assignment.id).one()
    session.delete(assign)
    session.commit()
    return assign