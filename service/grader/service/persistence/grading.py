from grader.service.persistence.database import DataBaseManager
from sqlalchemy import text
from sqlalchemy.orm import Session
from grader.common.models.user import User
import datetime
import json

def get_score(subid: int):
    session = DataBaseManager.instance().create_session()

    select = text("SELECT score FROM feedback WHERE subid=:id")
    select = select.bindparams(id=subid)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res