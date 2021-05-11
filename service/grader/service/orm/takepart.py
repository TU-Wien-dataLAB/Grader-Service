from .base import Base, Serializable
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
import enum


class Scope(enum.IntEnum):
    student = 0
    tutor = 1
    instructor = 2
    admin = 3


class Role(Base, Serializable):
    __tablename__ = "takepart"
    username = Column(Integer, ForeignKey("user.name"), primary_key=True)
    lectid = Column(Integer, ForeignKey("lecture.id"), primary_key=True)
    role = Column(Enum(Scope), nullable=False)

    lecture = relationship("Lecture", back_populates="roles")
    user = relationship("User", back_populates="roles")
