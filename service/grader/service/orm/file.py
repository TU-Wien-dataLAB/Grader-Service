from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class File(Base, BaseMixin):
  __tablename__ = "file"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  assignid = Column(Integer, ForeignKey('assignment.id'))
  path = Column(String(255), nullable=False)
  exercise = Column(Boolean, nullable=False)          
  points = Column(Integer)

  assignment = relationship("Assignment", back_populates="files")
