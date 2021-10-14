import tornado
from api.models.submission import Submission as SubmissionModel
from orm.assignment import Assignment
from orm.base import DeleteState
from orm.submission import Submission
from orm.takepart import Role, Scope
from registry import VersionSpecifier, register_handler
from sqlalchemy.sql.expression import func
from tornado.httpclient import HTTPError

from handlers.base_handler import GraderBaseHandler, authorize


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        latest = self.get_argument("latest", None) == "true"
        instructor_version = self.get_argument("instructor-version", None) == "true"

        role = self.session.query(Role).get((self.user.name, lecture_id))
        if instructor_version and role.role < Scope.tutor:
            self.error_message = "Unauthorized"
            raise HTTPError(403)

        if instructor_version:
            assignment = self.session.query(Assignment).get(assignment_id)
            if assignment is None or assignment.deleted == DeleteState.deleted:
                self.error_message = "Not Found"
                raise HTTPError(404)
            submissions = []
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
            else:
                submissions = assignment.submissions
            user_map = {}
            sub: Submission
            for sub in submissions:
                if sub.username in user_map:
                    user_map[sub.username]["submissions"].append(sub)
                else:
                    user_map[sub.username] = {"user": sub.user, "submissions": [sub]}
            response = list(user_map.values())
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
                )
            else:
                submissions = role.user.submissions
            response = [
                {
                    "user": role.user,
                    "submissions": [
                        s for s in submissions if s.assignid == int(assignment_id)
                    ],
                }
            ]
        self.write_json(response)

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def post(self, lecture_id: int, assignment_id: int):
        body = tornado.escape.json_decode(self.request.body)
        sub_model = SubmissionModel.from_dict(body)
        sub = Submission()
        sub.date = sub_model.submitted_at
        sub.assignid = assignment_id
        sub.username = self.user.name
        sub.auto_status = sub_model.auto_status
        sub.manual_status = sub_model.manual_status
        sub.feedback_available = sub_model.feedback_available or False
        self.session.add(sub)
        self.session.commit()
        self.write_json(sub)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionObjectHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, submission_id: int):
        submission = self.session.query(Submission).get(submission_id)
        self.write_json(submission)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/properties\/?",
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionPropertiesHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, submission_id: int):
        submission = self.session.query(Submission).get(submission_id)
        if submission is None:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        if submission.properties is not None:
            self.write(submission.properties)
        else:
            self.error_message = "Not Found!"
            raise HTTPError(404)

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int, submission_id: int):
        submission = self.session.query(Submission).get(submission_id)
        if submission is None:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        properties_string: str = self.request.body.decode("utf-8")
        submission.properties = properties_string
        self.session.commit()
        self.write_json(submission)
