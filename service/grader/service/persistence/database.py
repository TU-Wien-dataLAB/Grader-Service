from traitlets.config.configurable import LoggingConfigurable
from traitlets.traitlets import Unicode
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os


class DataBaseManager(LoggingConfigurable):

    database_url = Unicode("").tag(config=True)
    engine = create_engine(get_database_url(),echo=True)

    @staticmethod
    def get_database_url():
        return  "sqlite:///" + os.path.abspath(os.path.dirname(__file__) + "../../../../grader.db")

    @classmethod
    def create_session(cls):
        return Session(bind=cls.engine)