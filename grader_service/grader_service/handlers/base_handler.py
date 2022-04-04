import base64
import datetime
import functools
import json
import logging
import os
import shlex
import subprocess
import time
from typing import Any, Awaitable, Callable, List, Optional
from urllib.parse import ParseResult, urlparse

from traitlets import Type
from traitlets.config import SingletonConfigurable

from grader_service.api.models.base_model_ import Model
from grader_service.api.models.error_message import ErrorMessage
from grader_service.autograding.local_grader import LocalAutogradeExecutor
from grader_service.orm import Group, Assignment
from grader_service.orm.base import DeleteState, Serializable
from grader_service.orm.lecture import Lecture, LectureState
from grader_service.orm.takepart import Role, Scope
from grader_service.orm.user import User
from grader_service.registry import VersionSpecifier, register_handler
from grader_service.request import RequestService
from grader_service.server import GraderServer
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tornado import httputil, web
from tornado.escape import json_decode
from tornado.httpclient import HTTPClientError
from tornado.web import HTTPError
from tornado_sqlalchemy import SessionMixin


def authorize(scopes: List[Scope]):
    if not set(scopes).issubset({Scope.student, Scope.tutor, Scope.instructor}):
        return ValueError("Invalid scopes")

    # needs_auth = set(scopes) != {Scope.student, Scope.tutor, Scope.instructor}

    def wrapper(handler_method):
        @functools.wraps(handler_method)
        async def request_handler_wrapper(self: "GraderBaseHandler", *args, **kwargs):
            lect_id = self.path_kwargs.get("lecture_id", None)
            if "/permissions" in self.request.path:
                return await handler_method(self, *args, **kwargs)
            if (
                    lect_id is None
                    and "/lectures" in self.request.path
                    and self.request.method == "POST"
            ):
                # lecture name and semester is in post body
                try:
                    data = json_decode(self.request.body)
                    lect_id = (
                        self.session.query(Lecture)
                            .filter(Lecture.code == data["code"])
                            .one()
                            .id
                    )
                except MultipleResultsFound:
                    self.error_message = "Unauthorized"
                    raise HTTPError(403)
                except NoResultFound:
                    self.error_message = "Not Found"
                    raise HTTPError(404)
                except json.decoder.JSONDecodeError:
                    self.error_message = "Unauthorized"
                    raise HTTPError(403)
            elif (
                    lect_id is None
                    and "/lectures" in self.request.path
                    and self.request.method == "GET"
            ):
                return await handler_method(self, *args, **kwargs)

            role = self.session.query(Role).get((self.user.name, lect_id))
            if role is None or not role.role in scopes:
                self.log.warn(
                    f"User {self.user.name} tried to access {self.request.path} with insufficient privileges"
                )
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

        self.application: GraderServer = (
            self.application
        )  # add type hint for application
        hub_api_parsed: ParseResult = urlparse(self.application.hub_api_url)
        self.hub_request_service.scheme = hub_api_parsed.scheme
        (
            self.hub_request_service.host,
            self.hub_request_service.port,
        ) = httputil.split_host_and_port(hub_api_parsed.netloc)
        self.hub_api_base_path: str = hub_api_parsed.path

        self.error_message = "Unknown Error"
        self.has_auth = False
        self.log = self.application.log

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def prepare(self) -> Optional[Awaitable[None]]:
        await self.authenticate_user()

    def validate_parameters(self, *args):
        if len(self.request.arguments) == 0:
            return
        if len(set(self.request.arguments.keys()) - set(self.request.body_arguments) - set(args)) != 0:
            raise HTTPError(400, "Unknown arguments")

    @property
    def gitbase(self):
        app: GraderServer = self.application
        return os.path.join(app.grader_service_dir, "git")

    def get_assignment(self,lecture_id: int, assignment_id: int) -> Optional[Assignment] :
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == 1 or assignment.lectid != lecture_id:
            raise HTTPError(404)
        return assignment

    def construct_git_dir(self, repo_type: str, lecture: Lecture, assignment: Assignment) -> Optional[str]:
        """Helper method for every handler that needs to access git directories which returns
        the path of the repository based on the inputs or None if the repo_type is not recognized.
        """
        assignment_path = os.path.abspath(
            os.path.join(self.gitbase, lecture.code, assignment.name)
        )
        if repo_type == "source" or repo_type == "release":
            path = os.path.join(assignment_path, repo_type)
        elif repo_type in ["autograde", "feedback"]:
            type_path = os.path.join(assignment_path, repo_type, assignment.type)
            if assignment.type == "user":
                path = os.path.join(type_path, self.user.name)
            else:
                group = self.session.query(Group).get((self.user.name, lecture.id))
                if group is None:
                    self.error_message = "Not Found"
                    raise HTTPError(404)
                path = os.path.join(type_path, group.name)
        elif repo_type == "user":
            user_path = os.path.join(assignment_path, repo_type)
            path = os.path.join(user_path, self.user.name)
        elif repo_type == "group":
            group = self.session.query(Group).get((self.user.name, lecture.id))
            if group is None:
                self.error_message = "Not Found"
                raise HTTPError(404)
            group_path = os.path.join(assignment_path, repo_type)
            path = os.path.join(group_path, group.name)
        else:
            return None

        return path

    def _run_command(self, command, cwd=None, capture_output=False):
        """Starts a sub process and runs an cmd command

        Args:
            command str: command that is getting run.
            cwd (str, optional): states where the command is getting run. Defaults to None.
            capture_output (bool, optional): states if output is getting saved. Defaults to False.

        Raises:
            GitError: returns appropriate git error 

        Returns:
            str: command output
        """
        try:
            self.log.info(f"Running: {command}")
            ret = subprocess.run(shlex.split(command), check=True, cwd=cwd, capture_output=True)
            if capture_output:
                return str(ret.stdout, 'utf-8')
        except subprocess.CalledProcessError as e:
            self.log.error(e)
            raise HTTPError(500)
        except FileNotFoundError as e:
            self.log.error(e)
            raise HTTPError(404)

    async def authenticate_user(self):
        """
        This is a workaround for async authentication. `get_current_user` cannot be asynchronous and a request cannot be made in a blocking manner.
        This sets the `current_user` property before each request before being checked by the `authenticated` decorator.
        """
        token = self.get_request_token()
        if token is None:
            self.error_message = "Unauthorized"
            self.write_error(403)
            self.finish()
            return
            # raise HTTPError(403)

        start_time = time.monotonic()

        user = await self.authenticate_token_user(token)
        if user is None:
            self.log.warn("Request from unauthenticated user")
            self.error_message = "Unauthorized"
            self.write_error(403)
            self.finish()
            return
            # raise HTTPError(403)
        self.set_secure_cookie(token, json.dumps(user), expires_days=self.application.max_token_cookie_age_days)
        self.log.info(
            f'User {user["name"]} has been authenticated (took {(time.monotonic() - start_time) * 1e3:.2f}ms)')

        user_model = self.session.query(User).get(user["name"])
        if user_model is None:
            self.log.info(f'User {user["name"]} does not exist and will be created.')
            user_model = User(name=user["name"])
            self.session.add(user_model)
            self.session.commit()

        # user is authenticated by the cookie and the user exists in the database
        if self.authenticate_cookie_user(user):
            self.current_user = user_model
            return

        lecture_roles = {
            code: {"role": role}
            for code, role in [tuple(g.split(":", 1)) for g in user["groups"]]
        }

        for lecture_code in lecture_roles.keys():
            lecture = (
                self.session.query(Lecture)
                    .filter(Lecture.code == lecture_code)
                    .one_or_none()
            )
            if (
                    lecture is None
            ):  # create inactive lecture if no lecture with that name exists yet (code is set in create)
                self.log.info(
                    f"Adding inactive lecture with lecture_code {lecture_code}"
                )
                lecture = Lecture()
                lecture.code = lecture_code
                lecture.name = lecture_code
                lecture.state = LectureState.inactive
                lecture.deleted = DeleteState.active
                self.session.add(lecture)
        self.session.commit()

        self.session.query(Role).filter(Role.username == user["name"]).delete()
        for lecture_code, obj in lecture_roles.items():
            lecture = (
                self.session.query(Lecture)
                    .filter(Lecture.code == lecture_code)
                    .one_or_none()
            )
            if lecture is None:
                raise HTTPError(
                    500,
                    f"Could not find lecture with code: {lecture_code}. Inconsistent database state!",
                )
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
                self.set_secure_cookie(
                    user["name"], json.dumps(user), expires_days=max_age
                )
            return equal

    def get_request_token(self) -> Optional[str]:
        token = None
        for (k, v) in sorted(self.request.headers.get_all()):
            if k == "Authorization":
                name, value = v.split(" ")
                if name == "Token":
                    token = value
                    self.has_auth = True
                elif name == "Basic":
                    auth_decoded = base64.decodebytes(value.encode("ascii")).decode(
                        "ascii"
                    )
                    _, token = auth_decoded.split(
                        ":", 2
                    )  # we interpret the password as the token and ignore the username
                    self.has_auth = True
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
        except HTTPError as e:
            logging.getLogger(str(self.__class__)).error(e.reason)
            return None
        except HTTPClientError as e:
            logging.getLogger(str(self.__class__)).error(e.response.error)
            return None
        return user

    def write_json(self, obj) -> None:
        self.set_header("Content-Type", "application/json")
        chunk = GraderBaseHandler._serialize(obj)
        self.write(json.dumps(chunk))

    def write_error(self, status_code: int, **kwargs) -> None:
        self.clear()
        if status_code == 403 and not self.has_auth:
            status_code = 401
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


@register_handler(r"\/", VersionSpecifier.NONE)
class VersionHandler(GraderBaseHandler):
    async def get(self):
        self.write("1.0")


@register_handler(r"\/", VersionSpecifier.V1)
class VersionHandlerV1(GraderBaseHandler):
    async def get(self):
        self.write("1.0")


# This class exists to not avoid all request handlers to inherit from traitlets.config.Configurable
# and making all requests super slow. If a request handler needs configurable values, they can be accessed
# from this object.
class RequestHandlerConfig(SingletonConfigurable):
    autograde_executor_class = Type(default_value=LocalAutogradeExecutor,
                                    klass=object,  # TODO: why does using LocalAutogradeExecutor give subclass error?
                                    allow_none=False).tag(config=True)
