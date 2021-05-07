from grader.service.persistence.database import DataBaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.service import orm
import datetime
import json

def get_score(subid: int):
    session = DataBaseManager.instance().create_session()

    score = session.query(orm.Submission).filter(orm.Submission.id == subid).one().score
    session.commit()
    return score