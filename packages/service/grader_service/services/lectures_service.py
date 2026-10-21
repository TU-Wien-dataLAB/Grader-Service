from http import HTTPStatus

from sqlalchemy import select
from tornado.web import HTTPError

from grader_service.api.models import LectureListItemDto, LectureDetailDto, LectureUpdateDto
from grader_service.orm.base import DeleteState
from grader_service.orm.lecture import LectureState
from grader_service.orm.takepart import Scope
from grader_service.services.base_service import BaseService
from grader_service.orm import User, Lecture, Role
from grader_service.services.mappers.lectures_mapper import (
    to_lecture_list_item_dto,
    to_lecture_detail_dto,
)


class LecturesService(BaseService):
    # TODO: add filtering, sorting and pagination params
    def get_all_lectures(
        self, complete: str, instructor_view: str, user: User
    ) -> list[LectureListItemDto]:
        with self.session_maker() as session:
            stmt = select(Lecture)
            if complete is not None:
                state = LectureState.complete if complete == "true" else LectureState.active
                stmt = stmt.where(Lecture.state == state)

            if not user.is_admin:
                stmt = stmt.join(Role).where(
                    Role.user_id == user.id, Lecture.deleted == DeleteState.active
                )

                if instructor_view == "true" and self.has_elevated_permissions(session, user):
                    stmt = stmt.where(Role.role.in_([Scope.instructor, Scope.tutor]))

            lectures = session.scalars(stmt).all()
            ids = [lec.id for lec in lectures]
            a_counts = self.get_assignment_counts(session, ids)
            s_counts = self.get_student_counts(session, ids)

            return [
                to_lecture_list_item_dto(
                    lec,
                    a_counts.get(lec.id, 0),
                    s_counts.get(lec.id, 0) if instructor_view == "true" else None,
                )
                for lec in lectures
            ]

    def get_lecture_by_id(self, lecture_id: int, user: User) -> LectureDetailDto:
        with self.session_maker() as session:
            lecture = self.get_lecture(session, lecture_id)

            if not user.is_admin:
                if lecture.deleted == DeleteState.deleted:
                    raise HTTPError(HTTPStatus.NOT_FOUND, reason="Lecture not found")
            return to_lecture_detail_dto(lecture)

    def update_lecture(self, lecture_id: int, lecture_dto: LectureUpdateDto):
        with self.session_maker() as session:
            lecture = self.get_lecture(session, lecture_id)

            lecture.name = lecture_dto.name
            lecture.state = LectureState.complete if lecture_dto.complete else LectureState.active

            session.commit()
            return to_lecture_detail_dto(lecture)
