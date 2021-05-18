from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from grader.service.orm.assignment import Assignment
from grader.service.orm.submission import Submission
from grader.service.orm.takepart import Role, Scope
from grader.common.models.error_message import ErrorMessage
from sqlalchemy.sql.expression import false
from tornado import web
from jupyter_server.utils import url_path_join
import tornado
import json


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?"
)
class SubmissionHandler(GraderBaseHandler):
    @authenticated
    def get(self, lecture_id: int, assignment_id: int):
        latest = self.get_argument("latest", False)
        instructor_version = self.get_argument("instructor-version", False)

        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None or (instructor_version and role.role < Scope.tutor):
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return

        if instructor_version:
            assignment = self.session.query(Assignment).get(assignment_id)
            if assignment is None:
                self.write_error(404, "Not found!")
                return
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
        self.write(response)

    @authenticated
    def post(self, lecture_id: int, assignment_id: int):
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/?"
)
class FeedbackHandler(GraderBaseHandler):
    @authenticated
    def get(self, lecture_id: int, assignment_id: int):
        latest = self.get_argument("latest", False)
        instructor_version = self.get_argument("instructor-version", False)
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/feedback\/(?P<feedback_id>\d*)\/?"
)
class FeedbackObjectHandler(GraderBaseHandler):
    async def get(self, lecture_id: int, assignment_id: int, feedback_id: int):
        pass
