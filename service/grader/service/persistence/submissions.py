from typing import List
from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.submission import Submission
from sqlalchemy.sql import text
import datetime
import json 

def get_submissions(user: User, assignid: int,  latest: bool) -> List[Submission]:
    session = DataBaseManager.instance().create_session()

    select = ''
    if latest:
        select = text("SELECT * FROM submission WHERE assignid=:id AND username=:name ORDER BY date DESC LIMIT 1") 
    else:
        select = text("SELECT * FROM submission WHERE assignid=:id AND username=:name ORDER BY date DESC")
    select = select.bindparams(id=assignid, name=user.name)
    res = session.execute(select)
    res = [dict(x) for x in res]
    res = [Submission.from_dict({"id": d["id"], "submitted_at": d["date"], "status": d["status"]} for d in res)]
    session.commit()
    return res


def submit_assignment(user: User, assignid: int) -> None:
    session = DataBaseManager.instance().create_session()

    insert = text("INSERT INTO 'submission' ('date','assignid','username') VALUES (:date,:id,:name)")
    insert = insert.bindparams(date=datetime.date.today(), id=assignid, name=user.name)
    session.execute(insert)
    session.commit()
