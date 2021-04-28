from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_submissions(assignid: int, user: User):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM submission WHERE assignid=%i AND userid=%i ORDER BY date DESC" % (assignid, user.id)
    #TODO: make it to submission
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

#print(get_submissions(1,User(1,"user1")))