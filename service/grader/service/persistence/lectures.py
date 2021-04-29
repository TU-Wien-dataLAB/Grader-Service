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
    insert = 'INSERT INTO "lecture" ("name","semester","code") VALUES ("%s","%s","%s")' % (lecture.name,lecture.semester,lecture.code) 
    session.execute(insert)

    select = 'SELECT id FROM lecture WHERE lecture.name="%s"' % (lecture.name)
    select = session.execute(select)
    id = [r[0] for r in select]

    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES ("%s",%i,"%s")' % (user.name, id[0],"instructor")
    session.execute(insert)

    session.commit()

def takepart_as_student(user: User, lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES ("%s",%i,"%s")' % (user.name, lectid,"student")
    session.execute(insert)

def takepart_as_instructor(user: User, lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    insert = 'INSERT INTO "takepart" ("username","lectid","role") VALUES ("%s",%i,"%s")' % (user.name, lectid,"instructor")
    session.execute(insert)

def update_lecture(lecture: Lecture):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    update = 'UPDATE "lecture" SET name=%s, code=%s, complete=%r, semester=%s WHERE id=%i' % (lecture.name, lecture.code, lecture.complete, lecture.semester, lecture.id)
    session.execute(update)

def delete_lecture(lectid: int):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    delete = 'DELETE FROM "lecture" WHERE id=%i' % lectid
    session.execute(delete)