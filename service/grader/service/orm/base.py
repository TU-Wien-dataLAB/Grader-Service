from sqlalchemy.ext.declarative import declarative_base
from grader.common.models.base_model_ import Model

Base = declarative_base()

class Serializable(object):
    @property
    def model(self) -> Model:
        return Model()

    def serialize(self) -> dict:
        return self.model.to_dict()

    

    







  



