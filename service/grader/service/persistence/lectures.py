from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.service.persistence.database import DataBaseManager
import json

def get_lectures(user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = "SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE userid=%i" % user.id
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

# print(get_lectures(User(1,"user1")))