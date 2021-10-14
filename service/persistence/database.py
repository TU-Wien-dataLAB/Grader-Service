import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Int, Unicode


class DataBaseManager(SingletonConfigurable):

    # database URLs: dialect+driver://username:password@host:port/database
    db_dialect = Unicode("sqlite").tag(config=True)
    db_driver = Unicode(None, allow_none=True).tag(config=True)
    db_username = Unicode(None, allow_none=True).tag(config=True)
    db_password = Unicode(os.environ.get("GRADER_DB_PASSWORD"), allow_none=True).tag(
        config=True
    )
    db_host = Unicode("").tag(config=True)
    db_port = Int(None, allow_none=True).tag(config=True)
    db_path = Unicode("").tag(config=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = create_engine(self.get_database_url(), echo=True)
        self.log.info(f"DataBaseManager: url - { self.get_database_url() }")

    def get_database_url(self):
        url: str = self.db_dialect
        if self.db_driver is not None:
            url += "+" + self.db_driver
        url += "://"
        if self.db_username is not None:
            url += urllib.parse.quote_plus(self.db_username)
            if self.db_password is not None:
                url += ":" + urllib.parse.quote_plus(self.db_password)
        if self.db_username is not None:
            url += "@"
        url += self.db_host
        if self.db_port is not None:
            url += ":" + str(self.db_port)
        url += self.db_path
        return url

    def create_session(self):
        return Session(bind=self.engine)
