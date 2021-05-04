from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_files_of_assignment(user: User, assignid: int):
    session = DataBaseManager.create_session()

    select = "SELECT * FROM file WHERE assignid=:id"
    data = dict(id=assignid)
    res = session.execute(select,data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def get_exercises_of_assignment(user: User, assignid: int):
    session = DataBaseManager.create_session()

    select = "SELECT * FROM file WHERE assignid=:id AND exercise=true"
    data = dict(id=assignid)
    res = session.execute(select,data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res
