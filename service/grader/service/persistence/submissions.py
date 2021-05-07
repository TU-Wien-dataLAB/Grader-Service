from typing import List
from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.submission import Submission
from sqlalchemy.sql import text
from grader.service import orm
import datetime
import json 

def get_submissions(user: User, assignid: int,  latest: bool) -> List[Submission]:
    session = DataBaseManager.instance().create_session()
    select = session.query(orm.Submission).filter(orm.Submission.username == user.name, orm.Submission.assignid == assignid).all()
    res = [dict(x) for x in select]
    res = [Submission.from_dict({"id": d["id"], "submitted_at": d["date"], "status": d["status"]} for d in res)]
    session.commit()
    return res


def submit_assignment(user: User, assignid: int) -> None:
    session = DataBaseManager.instance().create_session()

    submission = orm.Submission(username=user.name,date=datetime.datetime.today(),assignid=assignid)
    session.add(submission)
    session.commit()