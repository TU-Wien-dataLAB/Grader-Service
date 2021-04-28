from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_assignments(assignid: int, user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM submission WHERE assignid=%i AND userid=%i ORDER BY date DESC" % (assignid, user.id)
    #TODO: make it to submission
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

print(get_assignments(1,User(1,"user1")))