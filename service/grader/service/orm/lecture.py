from sqlalchemy.sql.schema import UniqueConstraint
from .base import Base, Serializable, DeleteState
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from grader.common.models import lecture
import enum

class LectureState(enum.IntEnum):
    inactive = 0
    active = 1
    complete = 2

class Lecture(Base, Serializable):
    __tablename__ = "lecture"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True, unique=False)
    semester = Column(String(255), nullable=False, unique=False)
    code = Column(String(255), nullable=True, unique=True)
    state = Column(Enum(LectureState), nullable=False, unique=False)
    deleted = Column(Enum(DeleteState), nullable=False, unique=False)


    assignments = relationship("Assignment", back_populates="lecture")
    roles = relationship("Role", back_populates="lecture")
    groups = relationship("Group",back_populates="lecture")

    @property
    def model(self) -> lecture.Lecture:
        return lecture.Lecture(
            id=self.id,
            name=self.name,
            code=self.code,
            complete=self.state == LectureState.complete,
            semester=self.semester,
        )

