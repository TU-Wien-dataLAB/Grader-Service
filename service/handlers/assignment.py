from registry import register_handler
from handlers.base_handler import GraderBaseHandler, authorize
from orm.assignment import Assignment
from orm.base import DeleteState
from orm.file import File
from orm.takepart import Role, Scope
from server import GraderServer
from models.assignment import Assignment as AssignmentModel
from sqlalchemy.orm.exc import ObjectDeletedError
import tornado
from tornado.web import HTTPError


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role.lecture.deleted == DeleteState.deleted:
            self.error_message = "Not Found"
            raise HTTPError(404)

        if (
            role.role == Scope.student
        ):  # students do not get assignments that are created
            assignments = (
                self.session.query(Assignment)
                .filter(
                    Assignment.lectid == role.lecture.id,
                    Assignment.deleted == DeleteState.active,
                    Assignment.status != "created",
                )
                .all()
            )
        else:
            assignments = [
                a for a in role.lecture.assignments if a.deleted == DeleteState.active
            ]
        self.write_json(assignments)

    @authorize([Scope.instructor])
    async def post(self, lecture_id: int):
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = Assignment()

        assignment.name = assignment_model.name
        assignment.lectid = lecture_id
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status
        assignment.points = 0
        assignment.deleted = DeleteState.active
        self.session.add(assignment)
        self.session.commit()
        self.write_json(assignment)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(GraderBaseHandler):
    @authorize([Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int):
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)

        assignment.name = assignment_model.name
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        instructor_version = self.get_argument("instructor-version", "false") == "true"
        metadata_only = self.get_argument("metadata-only", "false") == "true"

        role = self.session.query(Role).get((self.user.name, lecture_id))
        if instructor_version and role.role < Scope.instructor:
            raise HTTPError(403)
        assignment = self.session.query(Assignment).get(assignment_id)
        if (
            assignment is None
            or assignment.deleted == DeleteState.deleted
            or (role.role == Scope.student and assignment.status == "created")
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        self.write_json(assignment)

    @authorize([Scope.instructor])
    async def delete(self, lecture_id: int, assignment_id: int):
        try:
            assignment = self.session.query(Assignment).get(assignment_id)
            if assignment is None:
                raise HTTPError(404)
            if assignment.deleted == 1:
                raise HTTPError(404)
            assignment.deleted = 1
            self.session.commit()
        except ObjectDeletedError:
            raise HTTPError(404)
