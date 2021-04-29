from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_submissions(assignid: int, user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = 'SELECT * FROM "submission" WHERE assignid=%i AND username="%s" ORDER BY date DESC' % (assignid, user.name)
    #TODO: make it to submission
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

