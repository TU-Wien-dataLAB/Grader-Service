from typing import Any

from autograding.feedback import GenerateFeedbackExecutor
from autograding.local import LocalAutogradeExecutor
from orm.submission import Submission
from orm.takepart import Scope
from registry import VersionSpecifier, register_handler
from tornado.httpclient import HTTPError
from tornado.ioloop import IOLoop

from handlers.base_handler import GraderBaseHandler, authorize


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/?",
    version_specifier=VersionSpecifier.ALL,
)
class GradingBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/auto\/?",
    version_specifier=VersionSpecifier.ALL,
)
class GradingAutoHandler(GraderBaseHandler):
    def on_finish(self):
        # we do not close the session we just commit because LocalAutogradeExecutor still needs it
        if self.session:
            self.session.commit()

    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        submission = self.session.query(Submission).get(sub_id)
        if submission is None:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        executor = LocalAutogradeExecutor(
            self.application.grader_service_dir, submission
        )
        IOLoop.current().spawn_callback(executor.start)
        submission = self.session.query(Submission).get(sub_id)
        self.write_json(submission)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<sub_id>\d*)\/feedback\/?",
    version_specifier=VersionSpecifier.ALL,
)
class GenerateFeedbackHandler(GraderBaseHandler):
    def on_finish(self):
        # we do not close the session we just commit because GenerateFeedbackHandler still needs it
        if self.session:
            self.session.commit()

    async def get(self, lecture_id: int, assignment_id: int, sub_id):
        submission = self.session.query(Submission).get(sub_id)
        if submission is None:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        executor = GenerateFeedbackExecutor(
            self.application.grader_service_dir, submission
        )
        IOLoop.current().spawn_callback(executor.start)
        submission = self.session.query(Submission).get(sub_id)
        self.write_json(submission)
