from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import datetime
import json

def get_submissions(assignid: int, user: User, latest: bool):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = ''
    if latest:
        select = 'SELECT * FROM "submission" WHERE assignid=:id AND username=":name" ORDER BY date DESC LIMIT 1' 
    else:
        select = 'SELECT * FROM "submission" WHERE assignid=:id AND username=":name" ORDER BY date DESC' 
    data = dict(id=assignid, name=user.name)
    res = session.execute(select,data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res


def submit_assignment(assignid: int, user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    insert = 'INSERT INTO "submission" ("date","assignid","username") VALUES (":date",:id,":name")'
    data = dict(date=datetime.date.today(), id=assignid, name=user.name)
    session.execute(insert,data)
    session.commit()

