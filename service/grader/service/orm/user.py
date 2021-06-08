from .base import Base, Serializable
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class User(Base, Serializable):
  __tablename__ = 'user'
  name =  Column(String(255), primary_key=True)

  roles = relationship("Role", back_populates="user")
  submissions = relationship("Submission", back_populates="user")
  groups = relationship("Group", back_populates="user")

  def serialize(self):
      return {"name": self.name}