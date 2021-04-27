from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User

def get_assignments(lectid: int):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT * FROM assignment WHERE lectid=%i ORDER BY duedate DESC" % lectid
    #TODO: make it to assignment
    res = list(session.execute(select))
    session.commit()
    return res

print(get_assignments(1))