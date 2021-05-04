from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_files_of_assignment(user: User, assignid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM file WHERE assignid=:id")
    select = select.bindparams(id=assignid)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def get_exercises_of_assignment(user: User, assignid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * FROM file WHERE assignid=:id AND exercise=true")
    select = select.bindparams(id=assignid)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res
