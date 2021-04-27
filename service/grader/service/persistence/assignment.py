from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
import json

def get_assignments(lectid: int):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM assignment WHERE lectid=%i ORDER BY duedate ASC" % lectid
    #TODO: make it to assignment
    res = session.execute(select)
    res = json.dumps( [dict(ix) for ix in res] )
    session.commit()
    return res

# rint(get_assignments(1))