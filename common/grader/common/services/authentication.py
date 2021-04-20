from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import HTTPHeaders
from enum import Enum

def get_authenticated_header() -> HTTPHeaders:
  return HTTPHeaders()


def authenticate_header(header: HTTPHeaders) -> HTTPHeaders:
  return header


def get_token() -> str:
  return ""


class SecurityScope(Enum):
  INSTRUCTOR = "instructor",
  TUTOR = "tutor",
  STUDENT = "student"


def get_scope() -> SecurityScope:
  return SecurityScope.STUDENT
