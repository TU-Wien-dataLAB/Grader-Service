from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Unicode
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os


class DataBaseManager(SingletonConfigurable):

    database_url = Unicode("sqlite:///" + os.path.abspath(os.path.dirname(__file__) + "../../../../grader.db")).tag(config=True)

    def __init__(self):
        #super(self.__init__())
        self.engine = create_engine(self.database_url,echo=True)

    def get_database_url(self):
        return  "sqlite:///" + os.path.abspath(os.path.dirname(__file__) + "../../../../grader.db")

    def create_session(self):
        return Session(bind=self.engine)
