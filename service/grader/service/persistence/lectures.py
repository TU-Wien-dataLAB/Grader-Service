from typing import List, Optional, SupportsComplex
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from grader.common.models.user import User
from grader.common.models.lecture import Lecture
from grader.service.persistence.database import DataBaseManager
from grader.service import orm
from grader.service.persistence.user import user_exists, create_user


def get_lecture_model(lecture: Optional[orm.Lecture]) -> Optional[Lecture]:
    if lecture is None:
        return None
    model = Lecture()
    model.id = lecture.id
    model.name = lecture.name
    model.complete = lecture.complete
    model.code = lecture.code
    model.semester = lecture.semester
    return model

def get_orm_from_model(lecture: Lecture) -> orm.Lecture:
    orm_lecture = orm.Lecture()
    orm_lecture.id = lecture.id
    orm_lecture.name = lecture.name
    orm_lecture.complete = lecture.complete
    orm_lecture.code = lecture.code
    orm_lecture.semester = lecture.semester
    return orm_lecture

def get_lectures(user: User) -> List[Lecture]:
    session = DataBaseManager.instance().create_session()
    lectures: List[orm.Lecture] = session.query(orm.Lecture).filter(orm.Role.lectid == orm.Lecture.id and orm.Role.username == user.name).all()
    res = []
    for lecture in lectures:
        model = get_lecture_model(lecture)
        res.append(model)
    session.commit()
    return res

def get_lecture(user: User, lectid: int) -> Lecture:
    session = DataBaseManager.instance().create_session()
    lecture: orm.Lecture = session.query(orm.Lecture).filter(lectid == orm.Lecture.id and orm.Role.username == user.name).one()
    res = get_lecture_model(lecture)
    session.commit()
    return res

def create_lecture(lecture: Lecture) -> Lecture:
    session = DataBaseManager.instance().create_session()
    lecture = get_orm_from_model(lecture)
    session.add(lecture)
    session.flush() # sets lecture.id

    model = get_lecture_model(lecture)
    session.commit()
    return model

def add_user_to_lecture(user: User, lecture: Lecture, role: str) -> None:
    if not user_exists(user):
        create_user(user)
    session = DataBaseManager.instance().create_session()
    orm_role = orm.Role()
    orm_role.lectid = lecture.id
    orm_role.username = user.name
    orm_role.role = role
    session.add(orm_role)
    session.commit()


def update_lecture(lecture: Lecture) -> None:
    session = DataBaseManager.instance().create_session()
    lect = session.query(orm.Lecture).get(lecture.id) 
    for key, value in lecture.to_dict():
        if hasattr(orm.Lecture, key) and key != "id":
            setattr(lect, key, value)
    session.commit()

def delete_lecture(lectid: int) -> None:
    session = DataBaseManager.instance().create_session()
    lect = session.query(orm.Lecture).get(lectid)
    session.delete(lect)
    session.commit()
