
from typing import List, Set, Tuple
from tornado.web import RedirectHandler, RequestHandler


class Singleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
          cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
      return cls._instances[cls]


class HandlerPathRegistry(object, metaclass=Singleton):
  def __init__(self):
    self.registry = {}

  @property
  def path_set(self) -> Set[str]:
    return set(self.registry.values())

  @property
  def path_list(self) -> List[str]:
    return list(self.registry.values())

  @property
  def handler_list(self) -> List[Tuple[str, RequestHandler]]:
    return list(zip(self.registry.values(), self.registry.keys()))

  def has_path(self, cls) -> bool:
    return cls in self.registry

  def get_path(self, cls):
    return self.registry[cls]

  def add(self, cls, path: str):
    # check if class inherits from tornado RequestHandler
    if RequestHandler not in cls.__mro__:
        raise ValueError(
            "Incorrect base class. Class has to be extended from tornado 'RequestHandler' in order to be registered."
        )
    self.registry[cls] = path


def register_handler(cls, path: str):
  HandlerPathRegistry().add(cls, path)
  return cls