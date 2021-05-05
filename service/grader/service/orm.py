from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    name =  Column(String(255), primary_key=True)


class Feedback(Base):
  __tablename__ = "feedback"
  Column('id', Integer, primary_key=True, autoincrement=True)
  Column('score', Integer, nullable=False)

class Submission(Base):
  __tablename__ = "submission"
  Column('id', Integer, primary_key=True, autoincrement=True)
  Column('date', DateTime, nullable=False)
  Column('status', Enum('submitting', 'not_graded', 'automatically_graded', 'manually_graded'), default='submitting', nullable=False)
  Column('assignid', Integer, ForeignKey('assignment.id'))
  Column('username', Integer, ForeignKey('user.name'))

class Assignment(Base):
  __tablename__ = "assignment"
  Column('id', Integer, primary_key=True, autoincrement=True)
  Column('name',String(255), nullable=False)
  Column('lectid', Integer, ForeignKey('lecture.id'))
  Column('duedate', DateTime, nullable=False)
  Column('path', String(255), nullable=False)
  Column('points', Integer, nullable=False)
  Column('status', Enum('created', 'released', 'fetching', 'fetched', 'complete'), default='created')

class File(Base):
  __tablename__ = "file"
  Column('id', Integer, primary_key=True, autoincrement=True)
  Column('name', String(255), nullable=False)
  Column('assignid', Integer, ForeignKey('assignment.id'))
  Column('path', String(255), nullable=False)
  Column('exercise', Boolean, nullable=False)          
  Column('points', Integer)

class Role(Base):
  __tablename__ = "takepart"
  Column('username', Integer, ForeignKey('user.name'), primary_key=True)
  Column('lectid', Integer, ForeignKey('lecture.id'), primary_key=True)
  Column('role', String(255), nullable=False)

class Lecture(Base):
  __tablename__ = "lecture"
  Column('id', Integer, primary_key=True, autoincrement=True)
  Column('name',String(255), nullable=False, unique=True)
  Column('semester',String(255), nullable=False)
  Column('code', String(255), nullable=False)
  Column('complete',Boolean(), default=False)