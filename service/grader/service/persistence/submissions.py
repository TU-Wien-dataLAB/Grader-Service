from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from sqlalchemy.sql import text
import datetime
import json 

def get_submissions(assignid: int, user: User, latest: bool):
    session = DataBaseManager.instance().create_session()

    select = ''
    if latest:
        select = text("SELECT * FROM submission WHERE assignid=:id AND username=:name ORDER BY date DESC LIMIT 1") 
    else:
        select = text("SELECT * FROM submission WHERE assignid=:id AND username=:name ORDER BY date DESC")
    select = select.bindparams(id=assignid, name=user.name)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res


def submit_assignment(assignid: int, user: User):
    session = DataBaseManager.instance().create_session()

    insert = text("INSERT INTO 'submission' ('date','assignid','username') VALUES (:date,:id,:name)")
    insert = insert.bindparams(date=datetime.date.today(), id=assignid, name=user.name)
    session.execute(insert)
    session.commit()
