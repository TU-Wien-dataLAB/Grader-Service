from api.models.error_message import ErrorMessage
from registry import VersionSpecifier, register_handler
from orm.lecture import Lecture, LectureState
from orm.user import User
from orm.takepart import Role, Scope
from orm.base import DeleteState
from handlers.base_handler import GraderBaseHandler, authorize
from jupyter_server.utils import url_path_join
from sqlalchemy.orm import exc
import tornado
from api.models.lecture import Lecture as LectureModel
from tornado.httpclient import HTTPError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound, ObjectDeletedError


@register_handler(r"\/lectures\/?", VersionSpecifier.ALL)
class LectureBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self):
        semester = self.get_argument("semester", None)
        if semester is None:
            lectures = [
                role.lecture
                for role in self.user.roles
                if role.lecture.state == LectureState.active
            ]
        else:
            lectures = [
                role.lecture
                for role in self.user.roles
                if role.lecture.state == LectureState.active 
                and role.lecture.deleted == DeleteState.active 
                and role.lecture.semester == semester
            ]
        self.write_json(lectures)

    @authorize([Scope.instructor])
    async def post(self):
        body = tornado.escape.json_decode(self.request.body)
        lecture_model = LectureModel.from_dict(body)
        try:
            lecture = self.session.query(Lecture).filter(Lecture.code == lecture_model.code).one_or_none()
        except NoResultFound:
            self.error_message = "Not found"
            raise HTTPError(404)
        except MultipleResultsFound:
            self.error_message = "Error"
            raise HTTPError(400)
        
        lecture.name = lecture_model.name
        lecture.code = lecture_model.code
        lecture.state = LectureState.complete if lecture_model.complete else LectureState.active
        lecture.semester = lecture_model.semester
        lecture.deleted = DeleteState.active

        self.session.commit()
        self.write_json(lecture)


@register_handler(r"\/lectures\/(?P<lecture_id>\d*)\/?", VersionSpecifier.ALL)
class LectureObjectHandler(GraderBaseHandler):
    @authorize([Scope.instructor])
    async def put(self, lecture_id: int):
        body = tornado.escape.json_decode(self.request.body)
        lecture_model = LectureModel.from_dict(body)
        lecture = self.session.query(Lecture).get(lecture_id)

        lecture.name = lecture_model.name
        lecture.code = lecture_model.code
        lecture.state = LectureState.complete if lecture_model.complete else LectureState.active
        lecture.semester = lecture_model.semester

        self.session.commit()
        self.write_json(lecture)

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        self.write_json(role.lecture)

    @authorize([Scope.instructor])
    async def delete(self, lecture_id: int):
        try:
            lecture = self.session.query(Lecture).get(Lecture)
            if lecture is None:
                raise HTTPError(404)
            if lecture.deleted == 1:
                raise HTTPError(404)
            lecture.deleted = 1
            for a in lecture.assignments:
                a.deleted = 1
        except ObjectDeletedError:
            raise HTTPError(404)
