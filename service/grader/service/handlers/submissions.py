from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authorize
from grader.service.orm.assignment import Assignment
from grader.service.orm.submission import Submission
from grader.service.orm.takepart import Role, Scope
from grader.common.models.error_message import ErrorMessage
from sqlalchemy.sql.expression import false
from tornado import web
from jupyter_server.utils import url_path_join
import tornado
import json

from tornado.httpclient import HTTPError


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?"
)
class SubmissionHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    def get(self, lecture_id: int, assignment_id: int):
        latest = self.get_argument("latest", False)
        instructor_version = self.get_argument("instructor-version", False)

        role = self.session.query(Role).get((self.user.name, lecture_id))
        if instructor_version and role.role < Scope.tutor:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        if instructor_version:
            assignment = self.session.query(Assignment).get(assignment_id)
            if assignment is None:
                self.error_message = "Not Found"
                raise HTTPError(404)
            user_map = {}
            sub: Submission
            for sub in assignment.submissions:
                if sub.username in user_map:
                    user_map[sub.username]["submissions"].append(sub)
                else:
                    user_map[sub.username] = {"user": sub.user, "submissions": [sub]}
            response = user_map.values()
        else:
            response = [
                {
                    "user": role.user,
                    "submissions": [
                        s
                        for s in role.user.submissions
                        if s.assignid == assignment_id
                    ],
                }
            ]
        self.write_json(response)

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    def post(self, lecture_id: int, assignment_id: int):
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?"
)
class FeedbackHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    def get(self, lecture_id: int, assignment_id: int):
        latest = self.get_argument("latest", False)
        instructor_version = self.get_argument("instructor-version", False)
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/(?P<feedback_id>\d*)\/?"
)
class FeedbackObjectHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, feedback_id: int):
        pass
