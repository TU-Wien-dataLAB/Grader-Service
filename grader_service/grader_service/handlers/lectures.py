import tornado
from grader_service.api.models.lecture import Lecture as LectureModel
from grader_service.orm.base import DeleteState
from grader_service.orm.lecture import Lecture, LectureState
from grader_service.orm.assignment import Assignment
from grader_service.orm.takepart import Role, Scope
from grader_service.registry import VersionSpecifier, register_handler
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound, ObjectDeletedError
from tornado.web import HTTPError

from grader_service.handlers.base_handler import GraderBaseHandler, authorize


@register_handler(r"\/lectures\/?", VersionSpecifier.ALL)
class LectureBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self):
        """Returns all lectures the user can access
        """
        self.validate_parameters("active")
        active = self.get_argument("active", "true") == "true"

        state = LectureState.active if active else LectureState.inactive
        lectures = [
            role.lecture
            for role in self.user.roles
            if role.lecture.state == state
               and role.lecture.deleted == DeleteState.active
               and (True if active else role.role == Scope.instructor)
        ]

        self.write_json(lectures)

    @authorize([Scope.instructor])
    async def post(self):
        """Creates a new lecture from a "ghost"-lecture

        :raises HTTPError: throws err if "ghost"-lecture was not found
        """
        self.validate_parameters()
        body = tornado.escape.json_decode(self.request.body)
        lecture_model = LectureModel.from_dict(body)
        try:
            lecture = (
                self.session.query(Lecture)
                    .filter(Lecture.code == lecture_model.code)
                    .one_or_none()
            )
        except NoResultFound:
            self.error_message = "Not found"
            raise HTTPError(404)
        except MultipleResultsFound:
            self.error_message = "Error"
            raise HTTPError(400)

        lecture.name = lecture_model.name
        lecture.code = lecture_model.code
        lecture.state = (
            LectureState.complete if lecture_model.complete else LectureState.active
        )
        lecture.deleted = DeleteState.active

        self.session.commit()
        try:
            lecture = (
                self.session.query(Lecture)
                    .filter(Lecture.code == lecture_model.code)
                    .one_or_none()
            )
        except NoResultFound:
            self.error_message = "Not found"
            raise HTTPError(404)
        except MultipleResultsFound:
            self.error_message = "Error"
            raise HTTPError(400)
        self.write_json(lecture)


@register_handler(r"\/lectures\/(?P<lecture_id>\d*)\/?", VersionSpecifier.ALL)
class LectureObjectHandler(GraderBaseHandler):
    @authorize([Scope.instructor])
    async def put(self, lecture_id: int):
        """Updates a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """
        self.validate_parameters()
        body = tornado.escape.json_decode(self.request.body)
        lecture_model = LectureModel.from_dict(body)
        lecture = self.session.query(Lecture).get(lecture_id)

        lecture.name = lecture_model.name
        lecture.state = (
            LectureState.complete if lecture_model.complete else LectureState.active
        )

        self.session.commit()
        self.write_json(lecture)

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        self.validate_parameters()
        role = self.get_role(lecture_id)
        if role.lecture.deleted == DeleteState.deleted:
            self.error_message = "Not found"
            raise HTTPError(404)

        self.write_json(role.lecture)

    @authorize([Scope.instructor])
    async def delete(self, lecture_id: int):
        """ "Soft"-delete a lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :raises HTTPError: throws err if lecture was already deleted or was not found

        """
        self.validate_parameters()
        try:
            lecture = self.session.query(Lecture).get(lecture_id)
            if lecture is None:
                raise HTTPError(404)
            if lecture.deleted == 1:
                raise HTTPError(404)
            lecture.deleted = 1
            a: Assignment
            for a in lecture.assignments:
                if (len(a.submissions)) > 0 or a.status in ["released", "complete"]:
                    self.session.rollback()
                    raise HTTPError(400, "Cannot delete assignment")
                a.deleted = 1
            self.session.commit()
        except ObjectDeletedError:
            raise HTTPError(404)
        self.write("OK")


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/users\/?",
    version_specifier=VersionSpecifier.ALL,
)
class LectureStudentsHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        roles = self.session.query(Role).filter(Role.lectid == lecture_id).all()
        students = [r.username for r in roles if r.role == Scope.student]
        tutors = [r.username for r in roles if r.role == Scope.tutor]
        instructors = [r.username for r in roles if r.role == Scope.instructor]

        counts = {"instructors": instructors, "tutors": tutors, "students": students}
        self.write_json(counts)
