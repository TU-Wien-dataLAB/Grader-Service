from grader.service.persistence.database import DataBaseManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def create_user(user: User):
    engine = create_engine(DataBaseManager.get_database_url(), echo=True)
    session = Session(bind=engine)
    insert = 'INSERT INTO "user" ("name") VALUES ("%s")' % user.name
    session.execute(insert)
    session.commit()