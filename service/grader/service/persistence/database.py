from traitlets.config.configurable import LoggingConfigurable
from traitlets.traitlets import Unicode
import os


class DataBaseManager(LoggingConfigurable):

    database_url = Unicode("").tag(config=True)

    @staticmethod
    def get_database_url():
        return  "sqlite:///" + os.path.abspath(os.path.dirname(__file__) + "../../../../grader.db")