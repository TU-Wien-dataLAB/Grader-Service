from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
<<<<<<< HEAD
from grader.common.models.lecture import Lecture
=======
from grader.service.persistence.database import DataBaseManager
>>>>>>> 19c9b3d65a4fc595d85197ca1d798ef5676cdfbd
import json

def get_lectures(user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = "SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE userid=%i" % user.id
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def get_lecture(user: User, lectid: int):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = "SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE userid=%i AND lecture.id=%i" % (user.id,lectid)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def create_lecture(user: User, lecture: Lecture):
    engine = create_engine('sqlite:///grader.db', echo=True)
    session = Session(bind=engine)
    select = 'INSERT INTO "lecture" ("name","semester","code") VALUES ("%s","%s","%s")' % (lecture.name,lecture.semester,lecture.code) 
    session.execute(select)
    select = 'INSERT INTO "takepart" ("userid","lectid","role") VALUES (%i,%i,"%s")' % (user.id, lecture.id,"admin")
    session.execute(select)

    session.commit()


#print(get_lecture(User(1,"user1"),2))
create_lecture(User(1,"user1"),Lecture(name="lecture1",code="dsdsdd",complete=False,semester="WS22"))
print(get_lectures(User(1,"user1")))
