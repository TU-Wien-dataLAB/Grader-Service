from .base import Base, BaseMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship

class User(Base, BaseMixin):
  __tablename__ = 'user'
  name =  Column(String(255), primary_key=True)

  roles = relationship("Role", back_populates="user")