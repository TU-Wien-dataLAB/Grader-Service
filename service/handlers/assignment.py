import tornado
from api.models.assignment import Assignment as AssignmentModel
from orm.assignment import Assignment
from orm.base import DeleteState
from orm.takepart import Role, Scope
from registry import VersionSpecifier, register_handler
from sqlalchemy.orm.exc import ObjectDeletedError
from tornado.web import HTTPError

from handlers.base_handler import GraderBaseHandler, authorize


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?",
    version_specifier=VersionSpecifier.ALL,
)
class AssignmentBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        """ Returns all assignments of a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :raises HTTPError: throws err if lecture is deleted
        """
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
        """Creates a new assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role.lecture.deleted == DeleteState.deleted:
            self.error_message = "Not Found"
            raise HTTPError(404)
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = Assignment()

        assignment.name = assignment_model.name
        assignment.lectid = lecture_id
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status
        assignment.type = assignment_model.type
        assignment.points = 0
        assignment.deleted = DeleteState.active
        self.session.add(assignment)
        self.session.commit()
        self.write_json(assignment)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?",
    version_specifier=VersionSpecifier.ALL,
)
class AssignmentObjectHandler(GraderBaseHandler):
    @authorize([Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int):
        """Updates an assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if assignment was not found
        """
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)

        assignment.name = assignment_model.name
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status
        assignment.type = assignment_model.type
        self.session.commit()
        self.write_json(assignment)

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        """Returns a specific assignment of a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if assignment was not found
        """

        instructor_version = self.get_argument("instructor-version", "false") == "true"

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
        """Soft-Deletes a specific assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if assignment was not found or deleted
        """
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


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/properties\/?",
    version_specifier=VersionSpecifier.ALL,
)
class AssignmentPropertiesHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        """Returns the properties of a specific assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if the assignment or their properties were not found
        """
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        if assignment.properties is not None:
            self.write(assignment.properties)
        else:
            self.error_message = "Not Found!"
            raise HTTPError(404)

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int):
        """Updates the properties of a specific assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if the assignment was not found
        """
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        properties_string: str = self.request.body.decode("utf-8")
        assignment.properties = properties_string
        self.session.commit()
