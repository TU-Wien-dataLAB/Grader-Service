from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User

def get_lectures(user: User):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT lectid FROM takepart WHERE userid=%i" % user.id
    res = session.execute(select)
    lectures = []
    #TODO: make it to lectures[]
    for row in res:
        lectures.append(list(session.execute("SELECT * FROM lecture WHERE id=%i" % row.lectid)))
    session.commit()
    return lectures

print(get_lectures(User(1,"user1")))