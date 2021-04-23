from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
session = sessionmaker()
engine = create_engine('sqlite:///:mempry:', echo=True)
session.configure(bind=engine)
Session = Session()
