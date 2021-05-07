from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Table
from sqlalchemy.orm import relationship


Base = declarative_base()

class Submission(Base):
  __tablename__ = "submission"
  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(DateTime, nullable=False)
  status = Column(Enum('submitting', 'not_graded', 'automatically_graded', 'manually_graded'), default='submitting', nullable=False)
  score = Column(Integer, nullable=True)
  assignid = Column(Integer, ForeignKey('assignment.id'))
  username = Column(String(255), ForeignKey("user.name"))

  assignment = relationship("Assignment", back_populates="submissions")

class Assignment(Base):
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
  submissions = relationship(Submission, back_populates="assignment")

class File(Base):
  __tablename__ = "file"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  assignid = Column(Integer, ForeignKey('assignment.id'))
  path = Column(String(255), nullable=False)
  exercise = Column(Boolean, nullable=False)          
  points = Column(Integer)

  assignment = relationship("Assignment", back_populates="files")

role = Table('takepart', Base.metadata, Column('username',Integer, ForeignKey('user.name')), Column('lectid',Integer, ForeignKey('lecture.id')), Column('role',String(255), nullable=False))

class Lecture(Base):
  __tablename__ = "lecture"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False, unique=True)
  semester = Column(String(255), nullable=False)
  code = Column(String(255), nullable=False)
  complete = Column(Boolean(), default=False)

  assignments = relationship("Assignment", back_populates="lecture")
  users = relationship("User", secondary=role, back_populates="lectures")


class User(Base):
    __tablename__ = 'user'
    name =  Column(String(255), primary_key=True)

    lectures = relationship("Lecture", secondary=role, back_populates="users")
  

