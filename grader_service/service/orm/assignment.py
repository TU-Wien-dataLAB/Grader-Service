from service.api.models import assignment
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base, DeleteState, Serializable


class Assignment(Base, Serializable):
    __tablename__ = "assignment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum("user", "group"), nullable=False, server_default="user")
    lectid = Column(Integer, ForeignKey("lecture.id"))
    duedate = Column(DateTime, nullable=False)
    points = Column(Integer, nullable=True)
    status = Column(
        Enum("created", "pushed", "released", "fetching", "fetched", "complete"),
        default="created",
    )
    deleted = Column(Enum(DeleteState), nullable=False, unique=False)
    properties = Column(Text, nullable=True, unique=False)
    lecture = relationship("Lecture", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")

    @property
    def model(self) -> assignment.Assignment:
        assignment_model = assignment.Assignment(
            id=self.id,
            name=self.name,
            due_date=None
            if self.duedate is None
            else (self.duedate.isoformat("T", "milliseconds") + "Z"),
            status=self.status,
            type=self.type,
            points=self.points,
        )
        return assignment_model
