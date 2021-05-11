from grader.common.models.error_message import ErrorMessage
from grader.common.registry import register_handler
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from grader.service.orm import lecture
from grader.service.orm import assignment
from grader.service.orm.assignment import Assignment
from grader.service.orm.lecture import Lecture
from grader.service.orm.takepart import Role, Scope
from tornado import web
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment as AssignmentModel
from grader.service.persistence.assignment import get_assignments
from tornado_sqlalchemy import SessionMixin
import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(SessionMixin, GraderBaseHandler):
    @authenticated
    def get(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return

        self.write(role.lecture.assignments)

    @authenticated
    def post(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        if role.role < Scope.instructor:
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return

        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = Assignment()

        assignment.name = assignment_model.name
        assignment.lectid = lecture_id
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status

        self.session.commit()
        self.write(assignment)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(SessionMixin, GraderBaseHandler):
    @authenticated
    def put(self, lecture_id: int, assignment_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        if role.role < Scope.instructor:
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return

        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return

        assignment.name = assignment_model.name
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status

    @authenticated
    def get(self, lecture_id: int, assignment_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        self.write(assignment)

    @authenticated
    def delete(self, lecture_id: int, assignment_id: int):
        pass # TODO: set delete action in database


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/file\/(?P<file_id>\d*)\/?"
)
class AssignmentDataHandler(SessionMixin, GraderBaseHandler):
    @authenticated
    def get(self, lecture_id: int, assignment_id: int, file_id: int):
        pass # TODO: return binary file content
