from .base import Base, Serializable
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from api.models import submission

class Submission(Base, Serializable):
  __tablename__ = "submission"
  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(DateTime, nullable=False)
  status = Column(Enum('submitting', 'not_graded', 'automatically_graded', 'manually_graded'), default='submitting', nullable=False)
  score = Column(Integer, nullable=True)
  assignid = Column(Integer, ForeignKey('assignment.id'))
  username = Column(String(255), ForeignKey("user.name"))
  commit_hash = Column(String(length=40), nullable=False),

  assignment = relationship("Assignment", back_populates="submissions")
  user = relationship("User", back_populates="submissions")

  @property
  def model(self) -> submission.Submission:
      return submission.Submission(id=self.id, submitted_at=self.date, status=self.status, score=self.score)