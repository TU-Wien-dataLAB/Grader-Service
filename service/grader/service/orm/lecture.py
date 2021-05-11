from sqlalchemy.sql.visitors import _generate_dispatch
from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
# from grader.service.orm.assignment import Assignment
# from grader.service.orm.file import Role

class Lecture(Base, BaseMixin):
    __tablename__ = "lecture"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    semester = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    complete = Column(Boolean(), default=False)

    assignments = relationship("Assignment", back_populates="lecture")
    roles = relationship("Role", back_populates="lecture")

