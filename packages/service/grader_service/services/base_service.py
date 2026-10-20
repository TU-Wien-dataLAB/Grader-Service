from http import HTTPStatus
from typing import Optional

from sqlalchemy import select, func

from grader_service.errors import APIError
from grader_service.orm import Role, User, Lecture, Assignment
from grader_service.orm.base import DeleteState
from grader_service.orm.takepart import Scope


class BaseService:
    def __init__(self, session_maker, file_service):
        self.session_maker = session_maker
        self.file_service = file_service

    def get_role(self, lecture_id: int, user: User, session) -> Role:
        role: Optional[Role] = session.get(Role, (user.id, lecture_id))
        if role is None:
            raise APIError(HTTPStatus.NOT_FOUND, "No role found")
        return role

    def has_elevated_permissions(self, session, user: User):
        stmt = select(
            select(Lecture)
            .join(Role)
            .where(
                Role.user_id == user.id,
                Role.role.in_([Scope.instructor, Scope.tutor]),
                Lecture.deleted == DeleteState.active,
            )
            .exists()
        )
        return session.execute(stmt).scalar()

    def get_assignment_counts(self, session, lecture_ids):
        stmt = (
            select(Assignment.lectid, func.count())
            .where(Assignment.lectid.in_(lecture_ids))
            .group_by(Assignment.lectid)
        )
        return dict(session.execute(stmt).all())

    def get_student_counts(self, session, lecture_ids):
        stmt = (
            select(Role.lectid, func.count())
            .where(Role.lectid.in_(lecture_ids), Role.role == Scope.student)
            .group_by(Role.lectid)
        )
        return dict(session.execute(stmt).all())
