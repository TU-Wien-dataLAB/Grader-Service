import functools
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import ParseResult, urlparse
import json
import logging
from grader.common.models.error_message import ErrorMessage
from grader.service.orm.lecture import Lecture, LectureState
from grader.service.orm.assignment import Assignment
from grader.service.orm.takepart import Role
from grader.service.orm.user import User
from grader.common.services.request import RequestService
from grader.service.main import GraderService
from grader.service.server import GraderServer
from jupyterhub.services.auth import HubAuthenticated
from sqlalchemy.sql.expression import select
from tornado import httputil, web
from tornado.web import HTTPError
from grader.service.persistence.user import user_exists, create_user
from grader.service.orm.base import Serializable
from grader.common.models.base_model_ import Model
from tornado_sqlalchemy import SessionMixin
import datetime


class GraderBaseHandler(SessionMixin, web.RequestHandler):
    request_service = RequestService()
    hub_request_service = RequestService()

    def __init__(
        self,
        application: GraderServer,
        request: httputil.HTTPServerRequest,
        **kwargs: Any,
    ) -> None:
        super().__init__(application, request, **kwargs)

        self.application: GraderServer = self.application # add type hint for application
        hub_api_parsed: ParseResult = urlparse(self.application.hub_api_url)
        self.hub_request_service.scheme = hub_api_parsed.scheme
        (
            self.hub_request_service.host,
            self.hub_request_service.port,
        ) = httputil.split_host_and_port(hub_api_parsed.netloc)
        self.hub_api_base_path: str = hub_api_parsed.path

    async def prepare(self) -> Optional[Awaitable[None]]:
        """
        This is a workaround for async authentication. `get_current_user` cannot be asyncronous and a request cannot be made in a blocking manner.
        This sets the `current_user` property before each request before being checked by the `authenticated` decorator.
        """
        # TODO: add sessions to user requests
        user = await self.get_current_user_async()
        if user is None:
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return
        user_model = self.session.query(User).get(user["name"])
        if user_model is None:
            logging.getLogger("RequestHandler").info(
                f'User {user["name"]} does not exist and will be created.'
            )
            user_model = User(name=user["name"])
            self.session.add(user_model)
            self.session.commit()
        
        lecture_roles = {n:{"semester": s, "role": r} for n, s, r in [tuple(g.split("__", 2)) for g in  user["groups"]]}

        for lecture_name, obj in lecture_roles.items():
            lecture_models = self.session.query(Lecture).filter(Lecture.name == lecture_name, Lecture.semester == obj["semester"]).all()
            if len(lecture_models) == 0: # create inactive lecture if no lecture with that name exists yet (code is set in create)
                lecture = Lecture()
                lecture.name = lecture_name
                lecture.semester = obj["semester"]
                lecture.state = LectureState.inactive
                self.session.add(lecture)
        self.session.commit()
        
        self.session.query(Role).filter(Role.username == user["name"]).delete()
        for lecture_name, obj in lecture_roles.items():
            lecture = self.session.query(Lecture).filter(Lecture.name == lecture_name, Lecture.semester == obj["semester"]).one_or_none()
            if lecture is None:
                raise HTTPError(500, f'Could not find lecture with name: {lecture_name} and semester {obj["semester"]}. Inconsistent database state!')
            role = Role()
            role.username = user["name"]
            role.lectid = lecture.id
            role.role = obj["role"]
            self.session.add(role)
        self.session.commit()

        self.current_user = user_model

    async def get_current_user_async(self):
        token = None
        for (k, v) in sorted(self.request.headers.get_all()):
            if k == "Token":
                token = v
        if not token:  # request has to have an Authorization token for JupyterHub
            return None

        try:
            user: dict = await self.hub_request_service.request(
                "GET",
                self.hub_api_base_path + f"/authorizations/token/{token}",
                header={"Authorization": f"token {self.application.hub_api_token}"},
            )
            if user["kind"] != "user":
                return None
        except Exception as e:
            logging.getLogger().error(e)
            return None
        return user

    def write(self, obj) -> None:
        chunk = GraderBaseHandler._serialize(obj)
        super().write(json.dumps(chunk))
    
    def write_error(self, status_code: int, obj) -> None:
        self.clear()
        self.set_status(status_code)
        self.write(obj)

    @classmethod
    def _serialize(cls, obj: object):
        if isinstance(obj, list):
            return [cls._serialize(o) for o in obj]
        if isinstance(obj, dict):
            return {k: cls._serialize(v) for k, v in obj.items()}
        if isinstance(obj, tuple):
            return tuple(cls._serialize(o) for o in obj)
        if isinstance(obj, Serializable):
            return cls._serialize(obj.serialize())
        if isinstance(obj, (str, int, float, complex)) or obj is None:
            return obj
        if isinstance(obj, datetime.datetime):
            return str(obj)
        if isinstance(obj, Model):
            return cls._serialize(obj.to_dict())
        return None

    @property
    def user(self) -> User:
        return self.current_user


def authenticated(
    method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Optional[Awaitable[None]]]:
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, an `tornado.web.HTTPError` with cod 403 will be raised.
    """

    @functools.wraps(method)
    def wrapper(  # type: ignore
        self: GraderBaseHandler, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper
