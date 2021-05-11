from sqlalchemy.ext.declarative import declarative_base
from . import lecture,file,assignment,user,takepart,submission

Base = declarative_base()

class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        
    
    @classmethod
    def delete(cls, **kw):
        obj = cls(**kw)

    @classmethod
    def update(cls, **kw):
        obj = cls(**kw)









  



