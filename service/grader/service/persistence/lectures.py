from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.lecture import Lecture
from grader.service.persistence.database import DataBaseManager
import json

def get_lectures(user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = 'SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username="%s"' % user.name
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def get_lecture(user: User, lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = 'SELECT lecture.* FROM takepart INNER JOIN lecture ON lecture.id=takepart.lectid WHERE username="%s" AND lecture.id=%i' % (user.name,lectid)
    res = session.execute(select)
    res = json.dumps([dict(x) for x in res])
    session.commit()
    return res

def create_lecture(user: User, lecture: Lecture):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    select = 'INSERT INTO "lecture" ("name","semester","code") VALUES ("%s","%s","%s")' % (lecture.name,lecture.semester,lecture.code) 
    session.execute(select)

    select = 'INSERT INTO "takepart" ("username","lectid","role") VALUES ("%s",%i,"%s")' % (user.name, lecture.id,"admin")
    session.execute(select)

    session.commit()

