from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import datetime
import json

def get_score(subid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = 'SELECT score FROM feedback WHERE subid=:id'
    data = dict(id=subid)
    res = session.execute(select,data)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res