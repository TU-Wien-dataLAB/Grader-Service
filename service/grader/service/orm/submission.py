from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class Submission(Base, BaseMixin):
  __tablename__ = "submission"
  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(DateTime, nullable=False)
  status = Column(Enum('submitting', 'not_graded', 'automatically_graded', 'manually_graded'), default='submitting', nullable=False)
  score = Column(Integer, nullable=True)
  assignid = Column(Integer, ForeignKey('assignment.id'))
  username = Column(String(255), ForeignKey("user.name"))

  assignment = relationship("Assignment", back_populates="submissions")