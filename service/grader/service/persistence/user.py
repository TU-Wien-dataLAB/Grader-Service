from grader.service.persistence.database import DataBaseManager
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.common.models.user import User
from grader.service.orm import user
from grader.common.models.assignment import Assignment
import json

def create_user(user: User) -> None:
    session = DataBaseManager.instance().create_session()
    user_model = user.User(name=user.name)
    session.add(user_model)
    session.commit()


def user_exists(user: User) -> bool:
    session = DataBaseManager.instance().create_session()
    res = session.query(user.User).filter(user.User.name == user.name)
    return res.first() is not None

