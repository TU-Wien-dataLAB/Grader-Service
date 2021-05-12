from grader.service.persistence.database import DataBaseManager
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.service.orm.user import User
from grader.common.models.assignment import Assignment
import json

def create_user(user: User) -> None:
    session = DataBaseManager.instance().create_session()
    user_model = User(name=user.name)
    session.add(user_model)
    session.commit()


def user_exists(user: User) -> bool:
    session = DataBaseManager.instance().create_session()
    res = session.query(User).filter(User.name == user.name)
    return res.first() is not None

