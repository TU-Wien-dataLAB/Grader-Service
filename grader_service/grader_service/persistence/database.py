import os
import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Int, Unicode


class DataBaseManager(SingletonConfigurable):

    # database URLs: dialect+driver://username:password@host:port/database
    db_dialect = Unicode(os.getenv("GRADER_DB_DIALECT", "sqlite"), allow_none=False).tag(config=True)
    db_driver = Unicode(os.getenv("GRADER_DB_DRIVER"), allow_none=True).tag(config=True)
    db_username = Unicode(os.getenv("GRADER_DB_USERNAME"), allow_none=True).tag(config=True)
    db_password = Unicode(os.environ.get("GRADER_DB_PASSWORD"), allow_none=True).tag(
        config=True
    )
    db_host = Unicode(os.getenv("GRADER_DB_HOST"), allow_none=False).tag(config=True)
    db_port = Int(os.getenv("GRADER_DB_PORT"), allow_none=True).tag(config=True)
    db_path = Unicode(os.getenv("GRADER_DB_URL_PATH", "")).tag(config=True)

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
