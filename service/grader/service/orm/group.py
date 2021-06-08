from .base import Base, Serializable
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey



class Group(Base, Serializable):
    __tablename__ = "group"
    name = Column(String(255))
    username = Column(String(255), ForeignKey("user.name"), primary_key=True)
    lectid = Column(Integer, ForeignKey("lecture.id"), primary_key=True)


    lecture = relationship("Lecture", back_populates="groups")
    user = relationship("User", back_populates="groups")

