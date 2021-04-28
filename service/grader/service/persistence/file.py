from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_lectures(user: User, assignid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM file WHERE assignid=%i" % assignid
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

print(get_lectures(User(1,"user1"), 1))