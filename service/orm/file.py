from typing import Union
from .base import Base, Serializable
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from models.exercise import Exercise
from models.assignment_file import AssignmentFile


class File(Base, Serializable):
    __tablename__ = "file"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    assignid = Column(Integer, ForeignKey("assignment.id"))
    path = Column(String(255), nullable=False)
    exercise = Column(Boolean, nullable=False)
    points = Column(Integer)

    assignment = relationship("Assignment", back_populates="files")

    @property
    def model(self) -> Union[Exercise, AssignmentFile]:
        if self.exercise:
            model = Exercise(
                id=self.id,
                a_id=self.assignid,
                name=self.name,
                ex_type="nbgrader",
                points=self.points,
                path=self.path,
                hashcode=None,  # TODO: calculate hashcode of exercise
            )
        else:
            model = AssignmentFile(
                id=self.id,
                a_id=self.assignid,
                name=self.name,
                path=self.path,
                hashcode=None,
            )  # TODO: calculate hashcode

        return model
