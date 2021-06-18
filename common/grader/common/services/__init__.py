import datetime
from grader.service.orm.base import Serializable
from grader.common.models.base_model_ import Model


def serialize(obj: object):
    if isinstance(obj, list):
        return [serialize(o) for o in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, tuple):
        return tuple(serialize(o) for o in obj)
    if isinstance(obj, Serializable):
        return serialize(obj.serialize())
    if isinstance(obj, (str, int, float, complex)) or obj is None:
        return obj
    if isinstance(obj, datetime.datetime):
        return str(obj)
    if isinstance(obj, Model):
        return serialize(obj.to_dict())
    return None