from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class Assignment(Base, BaseMixin):
  __tablename__ = "assignment"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  lectid = Column(Integer, ForeignKey('lecture.id'))
  duedate = Column(DateTime, nullable=False)
  path = Column(String(255), nullable=False)
  points= Column(Integer, nullable=False)
  status = Column(Enum('created', 'released', 'fetching', 'fetched', 'complete'), default='created')

  lecture = relationship("Lecture", back_populates="assignments")
  files = relationship("File", back_populates="assignment")
  submissions = relationship("Submission", back_populates="assignment")