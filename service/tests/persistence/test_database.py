import os
from traitlets.config import Config
from grader.service.persistence.database import DataBaseManager


def test_get_url_dialect_host():
  c = Config()
  c.DataBaseManager.db_dialect = "sqlite"
  c.DataBaseManager.db_host = "/" + os.path.abspath(os.path.dirname(__file__) + "/../../grader.db")

  dbm: DataBaseManager = DataBaseManager.instance(config=c)
  assert dbm.db_dialect == c.DataBaseManager.db_dialect
  assert dbm.db_host == c.DataBaseManager.db_host

  assert dbm.get_database_url() == f"sqlite://{c.DataBaseManager.db_host}"


def test_get_url_full():
  # set values directly because import of driver libraries fails in __init__
  dbm: DataBaseManager = DataBaseManager.instance()
  dbm.db_dialect = "postgresql"
  dbm.db_driver = "pg8000"
  dbm.db_username = "dbuser"
  dbm.db_password = "kx%jj5/g"
  dbm.db_host = "pghost10"
  dbm.db_port = 2000
  dbm.db_path = "/appdb"

  assert dbm.get_database_url() == f'postgresql+pg8000://dbuser:kx%25jj5%2Fg@pghost10:2000/appdb'

def test_get_url_ignore_only_password():
  dbm: DataBaseManager = DataBaseManager.instance()
  dbm.db_dialect = "postgresql"
  dbm.db_driver = "pg8000"
  dbm.db_password = "kx%jj5/g"
  dbm.db_host = "pghost10"
  dbm.db_port = 2000
  dbm.db_path = "/appdb"

  assert dbm.get_database_url() == f'postgresql+pg8000://pghost10:2000/appdb'


def test_get_url_no_port():
  dbm: DataBaseManager = DataBaseManager.instance()
  dbm.db_dialect = "postgresql"
  dbm.db_driver = "pg8000"
  dbm.db_host = "pghost10"
  dbm.db_path = "/appdb"

  assert dbm.get_database_url() == f'postgresql+pg8000://pghost10/appdb'
