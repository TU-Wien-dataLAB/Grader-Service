import json

from .handler_utils import parse_ids
from ..orm.user import User
import tornado
from ..api.models.submission import Submission as SubmissionModel
from ..orm.assignment import Assignment
from ..orm.base import DeleteState
from ..orm.submission import Submission
from ..orm.takepart import Role, Scope
from ..registry import VersionSpecifier, register_handler
from sqlalchemy.sql.expression import func
from tornado.web import HTTPError
from grader_convert.gradebook.models import GradeBookModel

from .base_handler import GraderBaseHandler, authorize


def tuple_to_submission(t):
    s = Submission()
    (
        s.id,
        s.auto_status,
        s.manual_status,
        s.score,
        s.username,
        s.assignid,
        s.commit_hash,
        s.feedback_available,
        s.date,
    ) = t
    return s


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        """Return the submissions of an assignment

        Two query parameter: latest, instructor-version

        latest: only get the latest submissions of users
        instructor-version: if true, get the submissions of all users in lecture
                            if false, get own submissions

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if user is not authorized or the assignment was not found
        """
        lecture_id, assignment_id = parse_ids(lecture_id, assignment_id)
        self.validate_parameters("latest", "instructor-version")
        latest = self.get_argument("latest", None) == "true"
        instructor_version = self.get_argument("instructor-version", None) == "true"

        role: Role = self.session.query(Role).get((self.user.name, lecture_id))
        if instructor_version and role.role < Scope.tutor:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.lectid != lecture_id:
            self.error_message = "Not Found!"
            raise HTTPError(404)

        if instructor_version:
            if (
                assignment is None
                or assignment.deleted == DeleteState.deleted
                or assignment.lectid != lecture_id
            ):
                self.error_message = "Not Found"
                raise HTTPError(404)
            if latest:
                submissions = (
                    self.session.query(
                        Submission.id,
                        Submission.auto_status,
                        Submission.manual_status,
                        Submission.score,
                        Submission.username,
                        Submission.assignid,
                        Submission.commit_hash,
                        Submission.feedback_available,
                        func.max(Submission.date),
                    )
                    .filter(Submission.assignid == assignment_id)
                    .group_by(Submission.username)
                    .all()
                )
                submissions = [tuple_to_submission(t) for t in submissions]
            else:
                submissions = assignment.submissions
        else:
            if latest:
                submissions = (
                    self.session.query(
                        Submission.id,
                        Submission.auto_status,
                        Submission.manual_status,
                        Submission.score,
                        Submission.username,
                        Submission.assignid,
                        Submission.commit_hash,
                        Submission.feedback_available,
                        func.max(Submission.date),
                    )
                    .filter(
                        Submission.assignid == assignment_id,
                        Submission.username == role.username,
                    )
                    .group_by(Submission.username)
                    .all()
                )
                submissions = [tuple_to_submission(t) for t in submissions]
            else:
                submissions = (
                    self.session.query(
                        Submission
                    )
                    .filter(
                        Submission.assignid == assignment_id,
                        Submission.username == role.username,
                    )
                    .all()
                )
            
        self.write_json(submissions)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionObjectHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, submission_id: int):
        """Returns a specific submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        submission = self.session.query(Submission).get(submission_id)
        if (
            submission is None
            or submission.assignid != assignment_id
            or submission.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        self.write_json(submission)

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int, submission_id: int):
        """Updates a specific submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        body = tornado.escape.json_decode(self.request.body)
        sub_model = SubmissionModel.from_dict(body)
        sub = self.session.query(Submission).get(submission_id)
        if (
            sub is None
            or sub.assignid != assignment_id
            or sub.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        sub.date = sub_model.submitted_at
        sub.assignid = assignment_id
        sub.username = self.user.name
        sub.auto_status = sub_model.auto_status
        sub.manual_status = sub_model.manual_status
        sub.feedback_available = sub_model.feedback_available or False
        self.session.commit()
        self.write_json(sub)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/properties\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionPropertiesHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, submission_id: int):
        """
        Returns the properties of a submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        :raises HTTPError: throws err if the submission or their properties are not found
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        submission = self.session.query(Submission).get(submission_id)
        if (
            submission is None
            or submission.assignid != assignment_id
            or submission.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        if submission.properties is not None:
            self.write(submission.properties)
        else:
            self.error_message = "Not Found!"
            raise HTTPError(404)

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int, submission_id: int):
        """
        Updates the properties of a submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        :raises HTTPError: throws err if the submission are not found
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        submission = self.session.query(Submission).get(submission_id)
        if (
            submission is None
            or submission.assignid != assignment_id
            or submission.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        properties_string: str = self.request.body.decode("utf-8")
        try:
            score = GradeBookModel.from_dict(json.loads(properties_string)).score
        except:
            self.error_message = "Cannot parse properties file!"
            raise HTTPError(400)
        submission.score = score
        submission.properties = properties_string
        self.session.commit()
        self.write_json(submission)
