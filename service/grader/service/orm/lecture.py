from .base import Base, Serializable
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from grader.common.models import lecture


class Lecture(Base, Serializable):
    __tablename__ = "lecture"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    semester = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    complete = Column(Boolean(), default=False)

    assignments = relationship("Assignment", back_populates="lecture")
    roles = relationship("Role", back_populates="lecture")

    @property
    def model(self) -> lecture.Lecture:
        return lecture.Lecture(
            id=self.id,
            name=self.name,
            code=self.code,
            complete=self.complete,
            semester=self.semester,
        )

