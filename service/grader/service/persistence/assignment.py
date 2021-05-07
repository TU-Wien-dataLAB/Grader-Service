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
    session.commit()
    return select

#used for fechting specific assignment
def get_assignment(lectid: int, assignid: int):
    session = DataBaseManager.instance().create_session()

    select = session.query(orm.Assignment).filter(orm.Assignment.lectid == lectid, orm.Assignment.id == assignid).one()
    session.commit()
    return select

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

def delete_assignment(assignid: Assignment):
    session = DataBaseManager.instance().create_session()

    assign = session.query(orm.Assignment).filter(orm.Assignment.id==assignid).one()
    session.delete(assign)
    session.commit()
    return assign


def get_exercises(assignment: Assignment) -> List[Exercise]:
    session = DataBaseManager.instance().create_session()

    files = session.query(orm.Assignment).filter(orm.Assignment.files.exercise == True).all()

    res = [dict(ex) for ex in files]
    res = [Exercise.from_dict({"id": d["id"], "a_id": d["assignid"], "name": d["name"], "points": d["points"], "path": d["path"]} for d in res)]
    session.commit()
    return res

def get_files(assignment: Assignment) -> List[AssignmentFile]:
    session = DataBaseManager.instance().create_session()

    files = session.query(orm.Assignment).filter(orm.Assignment.files.exercise == False).all()

    res = [dict(ex) for ex in files]
    res = [AssignmentFile.from_dict({"id": d["id"], "a_id": d["assignid"], "name": d["name"], "path": d["path"]} for d in res)]
    session.commit()
    return res
