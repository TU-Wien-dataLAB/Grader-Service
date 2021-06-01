import functools
import re
from typing import Any, Awaitable, Callable, List, Optional
from urllib.parse import ParseResult, urlparse
import json
import logging
from grader.common.models.error_message import ErrorMessage
from grader.service.orm.lecture import Lecture, LectureState
from grader.service.orm.assignment import Assignment
from grader.service.orm.takepart import Role, Scope
from grader.service.orm.user import User
from grader.common.services.request import RequestService
from grader.service.main import GraderService
from grader.service.server import GraderServer
from jupyterhub.services.auth import HubAuthenticated
from sqlalchemy.sql.expression import select
from tornado import httputil, web
from tornado.web import HTTPError, RequestHandler
from grader.service.orm.base import Serializable
from grader.common.models.base_model_ import Model
from tornado_sqlalchemy import SessionMixin
from tornado.escape import json_decode
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import datetime
import base64


def authorize(scopes: List[Scope]):
    if not set(scopes).issubset({Scope.student, Scope.tutor, Scope.instructor}):
        return ValueError("Invalid scopes")
    needs_auth = set(scopes) != {Scope.student, Scope.tutor, Scope.instructor}

    def wrapper(handler_method):
        @functools.wraps(handler_method)
        async def request_handler_wrapper(self: 'GraderBaseHandler', *args, **kwargs):
            if needs_auth:
                lect_id = self.path_kwargs.get("lecture_id", None)
                if lect_id is None:
                    # lecture name and semester is in post body
                    try:
                        data = json_decode(self.request.body)
                        lect_id = self.session.query(Lecture).filter(Lecture.name == data["name"], Lecture.semester == data["semester"]).one().id
                    except MultipleResultsFound:
                        self.error_message = "Unauthorized"
                        raise HTTPError(403)
                    except NoResultFound:
                        self.error_message = "Not Found"
                        raise HTTPError(404)

                role = self.session.query(Role).get((self.user.name, lect_id))
                if role is None or not role.role in scopes:
                        self.error_message = "Unauthorized"
                        raise HTTPError(403)
            return await handler_method(self, *args, **kwargs)
        return request_handler_wrapper
    return wrapper

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

        self.error_message = None
        self.has_basic_auth = False

    async def prepare(self) -> Optional[Awaitable[None]]:
        await self.authenticate_user()


    async def authenticate_user(self):
        """
        This is a workaround for async authentication. `get_current_user` cannot be asyncronous and a request cannot be made in a blocking manner.
        This sets the `current_user` property before each request before being checked by the `authenticated` decorator.
        """
        token = self.get_request_token()
        if token is None:
            self.error_message = "Unauthorized"
            raise HTTPError(403)
        
        user = await self.authenticate_token_user(token)
        if user is None:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        user_model = self.session.query(User).get(user["name"])
        if user_model is None:
            logging.getLogger("RequestHandler").info(
                f'User {user["name"]} does not exist and will be created.'
            )
            user_model = User(name=user["name"])
            self.session.add(user_model)
            self.session.commit()
        
        # user is authenticated by the cookie and the user exists in the database
        if self.authenticate_cookie_user(user):
            self.current_user = user_model
            return 
        
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

    async def authenticate_token_user(self, token: str) -> Optional[dict]:
        max_token_age = self.application.max_token_cookie_age_days
        token_user = self.get_secure_cookie(token, max_age_days=max_token_age)
        if not token_user:
            user = await self.get_current_user_async(token)
            self.set_secure_cookie(token, json.dumps(user), expires_days=max_token_age)
            return user
        else:
            return json.loads(token_user)

    def authenticate_cookie_user(self, user: dict) -> bool:
        max_age = self.application.max_user_cookie_age_days
        cookie_user = self.get_secure_cookie(user["name"], max_age_days=max_age)
        if not cookie_user:
            self.set_secure_cookie(user["name"], json.dumps(user), expires_days=max_age)
            return False
        else:
            equal = user == json.loads(cookie_user)
            if not equal:
                self.set_secure_cookie(user["name"], json.dumps(user), expires_days=max_age)
            return equal

    def get_request_token(self) -> Optional[str]:
        token = None
        for (k, v) in sorted(self.request.headers.get_all()):
            if k == "Authorization":
                name, value = v.split(" ")
                if name == "Token":
                    token = value
                elif name == "Basic":
                    auth_decoded = base64.decodebytes(value.encode('ascii')).decode('ascii')
                    _, token = auth_decoded.split(':', 2) # we interpret the password as the token and ignore the username
                    self.has_basic_auth = True
                else:
                    token = None
                return token

    async def get_current_user_async(self, token) -> Optional[dict]:
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
    
    def write_json(self, obj) -> None:
        self.set_header('Content-Type', 'application/json')
        chunk = GraderBaseHandler._serialize(obj)
        self.write(json.dumps(chunk))
    
    def write_error(self, status_code: int, **kwargs) -> None:
        self.clear()
        self.set_status(status_code)
        self.write_json(ErrorMessage(self.error_message))

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
