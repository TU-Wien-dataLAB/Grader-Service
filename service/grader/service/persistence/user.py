from grader.service.persistence.database import DataBaseManager
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.common.models.user import User
from grader.common.models.assignment import Assignment
import json

def create_user(user: User) -> None:
    session = DataBaseManager.instance().create_session()

    insert = text("INSERT INTO 'user' ('name') VALUES (:name)")
    insert = insert.bindparams(name=user.name)

    session.execute(insert)
    session.commit()


def user_exists(user: User) -> bool:
    session = DataBaseManager.instance().create_session()

    select = text("SELECT * from 'user' where name = :name")
    select = select.bindparams(name=user.name)

    res = session.execute(select)
    return res.first() is not None

