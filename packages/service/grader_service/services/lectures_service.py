from sqlalchemy import select

from grader_service.api.models import LectureListItemDto
from grader_service.orm.base import DeleteState
from grader_service.orm.lecture import LectureState
from grader_service.orm.takepart import Scope
from grader_service.services.base_service import BaseService
from grader_service.orm import User, Lecture, Role
from grader_service.services.mappers.lectures_mapper import to_lecture_list_item_dto


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
