from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class Role(Base, BaseMixin):
  __tablename__ = "takepart"
  username = Column(Integer, ForeignKey('user.name'), primary_key=True)
  lectid = Column(Integer, ForeignKey('lecture.id'), primary_key=True)
  role = Column(String(255), nullable=False)

  lecture = relationship("Lecture", back_populates="roles")
  user = relationship("User", back_populates="roles")