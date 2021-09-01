
from typing import List, Set, Tuple
from tornado.web import RequestHandler
from jupyter_server.utils import url_path_join
import enum

class Singleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
          cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
      return cls._instances[cls]


class HandlerPathRegistry(object, metaclass=Singleton):
  registry = {}

  @property
  @staticmethod
  def path_set() -> Set[str]:
    return set(HandlerPathRegistry.registry.values())

  @property
  @staticmethod
  def path_list() -> List[str]:
    return list(HandlerPathRegistry.registry.values())

  @staticmethod
  def handler_list(base_url:str="/services/grader") -> List[Tuple[str, RequestHandler]]:
    return list(zip(
      [base_url.replace('/','\/') + path for path in HandlerPathRegistry.registry.values()], 
      HandlerPathRegistry.registry.keys()
    ))

  @staticmethod
  def has_path(cls) -> bool:
    return cls in HandlerPathRegistry.registry

  @staticmethod
  def get_path(cls):
    return HandlerPathRegistry.registry[cls]

  @staticmethod
  def add(cls, path: str):
    # check if class inherits from tornado RequestHandler
    if RequestHandler not in cls.__mro__:
        raise ValueError(
            "Incorrect base class. Class has to be extended from tornado 'RequestHandler' in order to be registered."
        )
    HandlerPathRegistry.registry[cls] = path


class VersionSpecifier(enum.Enum):
  ALL = "all"
  NONE = "none"
  V1 = "1"

def register_handler(path: str, version_specifier: VersionSpecifier=VersionSpecifier.NONE):
  if version_specifier == VersionSpecifier.ALL:
    # only supports single digit versions
    regex_versions = "".join([v.value for v in VersionSpecifier if v.value not in ['all', 'none']])
    v = r"(?:\/v[{}])?".format(regex_versions)
  elif version_specifier == VersionSpecifier.NONE or version_specifier is None:
    v = ""
  else:
    v = r"\/" + f"v{version_specifier.value}"
  path = v + path

  def _register_class(cls):
    HandlerPathRegistry().add(cls, path)
    return cls
  return _register_class
