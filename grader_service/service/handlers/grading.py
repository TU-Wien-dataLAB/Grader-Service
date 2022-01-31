from typing import Any

from traitlets import Type

from ..autograding.local_feedback import GenerateFeedbackExecutor
from ..autograding.grader_executor import GraderExecutor
from ..autograding.local_grader import LocalAutogradeExecutor
from .handler_utils import parse_ids
from ..orm.submission import Submission
from ..orm.takepart import Scope
from ..registry import VersionSpecifier, register_handler
from tornado.web import HTTPError
from tornado.ioloop import IOLoop

from .base_handler import GraderBaseHandler, authorize, RequestHandlerConfig


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
        """Starts the autograding process of a submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        :raises HTTPError: throws err if the submission was not found
        """
        lecture_id, assignment_id, sub_id = parse_ids(lecture_id, assignment_id, sub_id)
        self.validate_parameters()
        submission = self.session.query(Submission).get(sub_id)
        if (
                submission is None
                or submission.assignid != assignment_id
                or submission.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        executor = RequestHandlerConfig.instance().autograde_executor_class(
            self.application.grader_service_dir, submission, config=self.application.config
        )
        GraderExecutor.instance().submit(
            executor.start,
            lambda: self.log.info(f"Autograding of submission {submission.id} successful!")
        )
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
        """Starts the process of generating feedback for a submission

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param sub_id: id of the submission
        :type sub_id: int
        :raises HTTPError: throws err if the submission was not found
        """
        lecture_id, assignment_id, sub_id = parse_ids(lecture_id, assignment_id, sub_id)
        self.validate_parameters()
        submission = self.session.query(Submission).get(sub_id)
        if (
                submission is None
                or submission.assignid != assignment_id
                or submission.assignment.lectid != lecture_id
        ):
            self.error_message = "Not Found!"
            raise HTTPError(404)
        executor = GenerateFeedbackExecutor(
            self.application.grader_service_dir, submission, config=self.application.config
        )
        GraderExecutor.instance().submit(
            executor.start,
            lambda: self.log.info(f"Successfully generated feedback for submission {submission.id}!")
        )
        submission = self.session.query(Submission).get(sub_id)
        self.write_json(submission)
