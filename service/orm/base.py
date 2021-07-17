from sqlalchemy.ext.declarative import declarative_base
from models.base_model_ import Model
import enum

Base = declarative_base()

class Serializable(object):
    @property
    def model(self) -> Model:
        return Model()

    def serialize(self) -> dict:
        return self.model.to_dict()

class DeleteState(enum.IntEnum):
    active = 0
    deleted = 1
    

    







  



