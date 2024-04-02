# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
# grader_s/grader_s/handlers
import json
import shutil
import time

import isodate
import jwt
import os.path
import subprocess
from http import HTTPStatus
import tornado

from grader_service.handlers.git.base import RepoType
from grader_service.plugins.lti import LTISyncGrades
from grader_service.autograding.grader_executor import GraderExecutor
from grader_service.autograding.local_feedback import GenerateFeedbackExecutor
from grader_service.handlers.handler_utils import parse_ids
from grader_service.api.models.submission import Submission as SubmissionModel
from grader_service.api.models.assignment_settings import AssignmentSettings as AssignmentSettingsModel
from grader_service.orm.assignment import AutoGradingBehaviour
from grader_service.orm.assignment import Assignment
from grader_service.orm.lecture import Lecture
from grader_service.orm.submission import Submission
from grader_service.orm.submission_logs import SubmissionLogs
from grader_service.orm.submission_properties import SubmissionProperties
from grader_service.orm.takepart import Role, Scope
from grader_service.registry import VersionSpecifier, register_handler
from sqlalchemy.sql.expression import func
from tornado.web import HTTPError
from grader_service.convert.gradebook.models import GradeBookModel

from grader_service.handlers.base_handler import GraderBaseHandler, authorize, \
    RequestHandlerConfig
import datetime


def remove_points_from_submission(submissions):
    for s in submissions:
        if s.feedback_status not in ('generated', 'feedback_outdated'):
            s.score = None
    return submissions


@register_handler(
    path=r'\/lectures\/(?P<lecture_id>\d*)\/assignments' +
         r'\/(?P<assignment_id>\d*)\/submissions\/?',
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionHandler(GraderBaseHandler):
    """Tornado Handler class for http requests to
    /lectures/{lecture_id}/assignments/{assignment_id}/submissions.
    """

    def on_finish(self):
        # we do not close the session we just commit because we might run
        # LocalAutogradeExecutor or GenerateFeedbackExecutor in POST which
        # still need it
        pass

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        """Return the submissions of an assignment.

        Two query parameter: latest, instructor-version.

        latest: only get the latest submissions of users.
        instructor-version: if true, get the submissions of all users in
        lecture if false, get own submissions.

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if user is not authorized or
        the assignment was not found
        """
        lecture_id, assignment_id = parse_ids(lecture_id, assignment_id)
        self.validate_parameters("filter", "instructor-version", "format")
        submission_filter = self.get_argument("filter", "none")
        if submission_filter not in ["none", "latest", "best"]:
            raise HTTPError(HTTPStatus.BAD_REQUEST, reason="Filter parameter \
            has to be either 'none', 'latest' or 'best'")
        instr_version = self.get_argument("instructor-version", None) == "true"
        response_format = self.get_argument("format", "json")
        if response_format not in ["json", "csv"]:
            raise HTTPError(HTTPStatus.BAD_REQUEST, reason="Response format \
            can either be 'json' or 'csv'")

        role: Role = self.get_role(lecture_id)
        if instr_version and role.role < Scope.tutor:
            raise HTTPError(HTTPStatus.FORBIDDEN, reason="Forbidden")
        assignment = self.get_assignment(lecture_id, assignment_id)

        if instr_version:
            if submission_filter == 'latest':

                # build the subquery
                subquery = (
                    self.session.query(Submission.username,
                                       func.max(Submission.date).label(
                                           "max_date"))
                    .filter(Submission.assignid == assignment_id)
                    .group_by(Submission.username)
                    .subquery())

                # build the main query
                submissions = (
                    self.session.query(Submission)
                    .join(subquery,
                          (Submission.username == subquery.c.username) & (
                                  Submission.date == subquery.c.max_date) & (
                                  Submission.assignid == assignment_id))
                    .order_by(Submission.id)
                    .all())

            elif submission_filter == 'best':

                # build the subquery
                subquery = (
                    self.session.query(Submission.username,
                                       func.max(Submission.score).label(
                                           "max_score"))
                    .filter(Submission.assignid == assignment_id)
                    .group_by(Submission.username)
                    .subquery())

                # build the main query
                submissions = (
                    self.session.query(Submission)
                    .join(subquery,
                          (Submission.username == subquery.c.username) & (
                                  Submission.score == subquery.c.max_score) & (
                                  Submission.assignid == assignment_id))
                    .order_by(Submission.id)
                    .all())

            else:
                submissions = assignment.submissions
        else:
            if submission_filter == 'latest':
                # build the subquery
                subquery = (self.session.query(Submission.username,
                                               func.max(Submission.date).label(
                                                   "max_date"))
                            .filter(Submission.assignid == assignment_id)
                            .group_by(Submission.username)
                            .subquery())

                # build the main query
                submissions = (
                    self.session.query(Submission)
                    .join(subquery,
                          (Submission.username == subquery.c.username) & (
                                  Submission.date == subquery.c.max_date) & (
                                  Submission.assignid == assignment_id))
                    .filter(
                        Submission.assignid == assignment_id,
                        Submission.username == role.username, )
                    .order_by(Submission.id)
                    .all())

            elif submission_filter == 'best':

                # build the subquery
                subquery = (self.session.query(Submission.username, func.max(
                    Submission.score).label("max_score"))
                            .filter(Submission.assignid == assignment_id)
                            .group_by(Submission.username)
                            .subquery())

                # build the main query
                submissions = (
                    self.session.query(Submission)
                    .join(subquery,
                          (Submission.username == subquery.c.username) & (
                                  Submission.score == subquery.c.max_score) & (
                                  Submission.assignid == assignment_id))
                    .filter(
                        Submission.assignid == assignment_id,
                        Submission.username == role.username, )
                    .order_by(Submission.id)
                    .all())
            else:
                submissions = (
                    self.session.query(
                        Submission
                    )
                    .filter(
                        Submission.assignid == assignment_id,
                        Submission.username == role.username,
                    )
                    .order_by(Submission.id)
                    .all()
                )
        if response_format == "csv":
            # csv format does not include logs
            self.set_header("Content-Type", "text/csv")
            for i, s in enumerate(submissions):
                d = s.model.to_dict()
                if i == 0:
                    self.write(
                        ",".join((k for k in d.keys() if k != "logs")) + "\n")
                self.write(",".join(
                    (str(v) for k, v in d.items() if k != "logs")) + "\n")
        else:
            if not instr_version:
                submissions = remove_points_from_submission(submissions)

            self.write_json(submissions)
        self.session.close()  # manually close here because on_finish overwrite

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def post(self, lecture_id: int, assignment_id: int):
        """Create submission based on commit hash.

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :raises HTTPError: throws err if user is not authorized or
        the assignment was not found
        """
        lecture_id, assignment_id = parse_ids(lecture_id, assignment_id)
        self.validate_parameters()
        body = tornado.escape.json_decode(self.request.body)
        try:
            commit_hash = body["commit_hash"]
        except KeyError:
            raise HTTPError(400, reason="Commit hash not found in body")

        role = self.get_role(lecture_id)
        assignment = self.get_assignment(lecture_id, assignment_id)
        if assignment.status == "complete":
            raise HTTPError(HTTPStatus.BAD_REQUEST,
                            reason="Cannot submit completed assignment!")
        if role.role == Scope.student and assignment.status != "released":
            raise HTTPError(HTTPStatus.NOT_FOUND)
        submission_ts = datetime.datetime.utcnow()

        score_scaling = 1.0
        if assignment.duedate is not None:
            score_scaling = self.calculate_late_submission_scaling(assignment, submission_ts, role)

        if assignment.max_submissions:
            submissions = assignment.submissions
            usersubmissions = [s for s in submissions if
                               s.username == role.username]
            if len(usersubmissions) >= assignment.max_submissions and role.role < Scope.tutor:
                raise HTTPError(HTTPStatus.CONFLICT, reason="Maximum number \
                of submissions reached!")

        submission = Submission()
        submission.assignid = assignment.id
        submission.date = submission_ts
        submission.username = self.user.name
        submission.score_scaling = score_scaling

        git_server = self.application.git_server_cls.instance()
        if not git_server.commit_hash_exists(commit_hash, RepoType(assignment.type), self.user, assignment, submission):
            raise HTTPError(HTTPStatus.NOT_FOUND, reason="Commit not found")

        submission.commit_hash = commit_hash
        submission.auto_status = "not_graded"
        submission.manual_status = "not_graded"
        submission.feedback_status = "not_generated"

        automatic_grading = assignment.automatic_grading

        self.session.add(submission)
        self.session.commit()
        self.set_status(HTTPStatus.CREATED)
        self.write_json(submission)

        # If the assignment has automatic grading or fully
        # automatic grading perform necessary operations
        if automatic_grading in [AutoGradingBehaviour.auto,
                                 AutoGradingBehaviour.full_auto]:
            submission.auto_status = "pending"
            self.session.commit()

            self.set_status(HTTPStatus.ACCEPTED)
            executor = RequestHandlerConfig.instance() \
                .autograde_executor_class(
                self.application.grader_service_dir, submission,
                close_session=False, config=self.application.config
            )
            if automatic_grading == AutoGradingBehaviour.full_auto:
                submission.feedback_status = "generating"
                self.session.commit()

                feedback_executor = GenerateFeedbackExecutor(
                    self.application.grader_service_dir, submission,
                    config=self.application.config
                )

                async def feedback_and_sync():

                    GraderExecutor.instance().submit(feedback_executor.start)
                    lecture: Lecture = self.session.query(Lecture).get(lecture_id)

                    lti_plugin = LTISyncGrades.instance()
                    data = (lecture.serialize(), assignment.serialize(), [submission.serialize()])

                    if lti_plugin.check_if_lti_enabled(*data, sync_on_feedback=True):

                        try:
                            await lti_plugin.start(*data)
                        except Exception as e:
                            self.log.error("Could not sync grades: " + str(e))

                    else:
                        self.log.info("Skipping LTI plugin as it is not enabled")

                GraderExecutor.instance().submit(executor.start, on_finish=feedback_and_sync)

                # Trigger LTI Plugin
            else:
                GraderExecutor.instance().submit(
                    executor.start,
                    lambda: self.log.info(
                        f"Autograding task of submission \
                        {submission.id} exited!")
                )
        if automatic_grading == AutoGradingBehaviour.unassisted:
            self.session.close()

    @staticmethod
    def calculate_late_submission_scaling(assignment, submission_ts, role: Role) -> float:
        assignment_settings = AssignmentSettingsModel.from_dict(json.loads(assignment.settings))
        if assignment_settings.late_submission and len(assignment_settings.late_submission) > 0:
            scaling = 0.0
            if submission_ts <= assignment.duedate:
                scaling = 1.0
            else:
                for period in assignment_settings.late_submission:
                    late_submission_date = assignment.duedate + isodate.parse_duration(period.period)
                    if submission_ts < late_submission_date:
                        scaling = period.scaling
                        break
                if scaling == 0.0 and role.role < Scope.tutor:
                    raise HTTPError(HTTPStatus.CONFLICT,
                                    reason="Submission after last late submission period of assignment!")
        else:
            if submission_ts < assignment.duedate:
                scaling = 1.0
            else:
                if role.role < Scope.tutor:
                    raise HTTPError(HTTPStatus.CONFLICT, reason="Submission after due date of assignment!")
                else:
                    scaling = 0.0
        return scaling


@register_handler(
    path=r'\/lectures\/(?P<lecture_id>\d*)\/assignments\/' +
         r'(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/?',
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionObjectHandler(GraderBaseHandler):
    """Tornado Handler class for http requests to
    /lectures/{lecture_id}/assignments/{assignment_id}/submissions
    /{submission_id}.
    """

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Returns a specific submission.

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
        submission = self.get_submission(lecture_id, assignment_id,
                                         submission_id)
        if self.get_role(lecture_id).role == Scope.student \
                and submission.username != self.user.name:
            raise HTTPError(HTTPStatus.NOT_FOUND)
        self.write_json(submission)

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Updates a specific submission and returns the updated entity.

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
        sub = self.get_submission(lecture_id, assignment_id, submission_id)
        # sub.date = sub_model.submitted_at
        # sub.assignid = assignment_id

        role = self.get_role(lecture_id)
        if role.role >= Scope.instructor:
            sub.username = sub_model.username
        sub.auto_status = sub_model.auto_status
        sub.manual_status = sub_model.manual_status
        sub.edited = sub_model.edited
        sub.feedback_status = sub_model.feedback_status
        if sub_model.score_scaling is not None and sub.score_scaling != sub_model.score_scaling:
            sub.score_scaling = sub_model.score_scaling
            sub.score = sub_model.score_scaling * sub.grading_score
        self.session.commit()
        self.write_json(sub)


@register_handler(
    path=r'\/lectures\/(?P<lecture_id>\d*)\/assignments\/' +
         r'(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/logs\/?',
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionLogsHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Returns logs of a submission.

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        :raises HTTPError: throws err if the submission logs are not found
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        logs = self.session.query(SubmissionLogs).get(submission_id)
        if logs is not None:
            self.write_json(logs.logs)
        else:
            raise HTTPError(HTTPStatus.NOT_FOUND,
                            reason="Properties of submission were not found")


@register_handler(
    path=r'\/lectures\/(?P<lecture_id>\d*)\/assignments\/' +
         r'(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/' +
         r'properties\/?',
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionPropertiesHandler(GraderBaseHandler):
    """Tornado Handler class for http requests to
    /lectures/{lecture_id}/assignments/{assignment_id}/submissions/
    {submission_id}/properties.
    """

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Returns the properties of a submission,

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        :param submission_id: id of the submission
        :type submission_id: int
        :raises HTTPError: throws err if the submission or
        their properties are not found
        """
        lecture_id, assignment_id, submission_id = parse_ids(
            lecture_id, assignment_id, submission_id
        )
        properties = self.session.query(SubmissionProperties).get(
            submission_id)
        if properties is not None and properties.properties is not None:
            # delete source cells from properties if user is student
            if self.get_role(lecture_id).role == Scope.student:
                model = GradeBookModel.from_dict(
                    json.loads(properties.properties))
                for notebook in model.notebooks.values():
                    notebook.source_cells_dict = {}
                self.write(json.dumps(model.to_dict()))
            else:
                self.write(properties.properties)
        else:
            raise HTTPError(HTTPStatus.NOT_FOUND,
                            reason="Properties of submission were not found")

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Updates the properties of a submission.

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
        submission = self.get_submission(lecture_id, assignment_id,
                                         submission_id)
        properties_string: str = self.request.body.decode("utf-8")

        try:
            gradebook = GradeBookModel.from_dict(json.loads(properties_string))

            score = gradebook.score
            submission.grading_score = score
            submission.score = submission.score_scaling * score

        except Exception as e:
            self.log.info(e)
            raise HTTPError(HTTPStatus.BAD_REQUEST,
                            reason="Cannot parse properties file!")

        properties = SubmissionProperties(properties=properties_string,
                                          sub_id=submission.id)

        self.session.merge(properties)

        if submission.feedback_status == 'generated':
            submission.feedback_status = 'feedback_outdated'

        if submission.manual_status == 'manually_graded':
            submission.manually_graded = 'being_edited'

        self.session.commit()
        self.write_json(submission)

    # TODO: not used, remove?
    def get_extra_credit(self, gradebook):
        extra_credit = 0
        for notebook in gradebook.notebooks.values():
            for grades in notebook.grades:
                extra_credit += grades.extra_credit if \
                    grades.extra_credit is not None else 0
        self.log.info("Extra credit is " + str(extra_credit))
        return extra_credit


@register_handler(
    path=r'\/lectures\/(?P<lecture_id>\d*)\/assignments\/' +
         r'(?P<assignment_id>\d*)\/submissions\/(?P<submission_id>\d*)\/edit\/?',
    version_specifier=VersionSpecifier.ALL,
)
class SubmissionEditHandler(GraderBaseHandler):

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int,
                  submission_id: int):
        """Create or overwrites the repository which stores changes of
        submissions files
        :param lecture_id: lecture id
        :param assignment_id: assignment id
        :param submission_id: submission id
        :return:
        """
        lecture_id, assignment_id = parse_ids(lecture_id, assignment_id)
        self.validate_parameters()

        submission = self.get_submission(lecture_id, assignment_id,
                                         submission_id)
        assignment = submission.assignment
        lecture = assignment.lecture

        git_server = self.application.git_server_cls.instance()

        # Location of repository which will store edited submission files
        edit_repo_location = git_server.git_location(RepoType.EDIT, self.user, assignment, submission)

        # Location of repository of student which contains the submitted files
        submission_repo_location = git_server.git_location(RepoType(assignment.type), self.user, assignment, submission)

        # Creating repository
        if not git_server.repo_exists(RepoType.EDIT, self.user, assignment, submission):
            git_server.create_repo(RepoType.EDIT, self.user, assignment, submission)

        # Create temporary paths to copy the submission
        # files in the edit repository
        tmp_path = os.path.join(
            self.application.grader_service_dir,
            "tmp",
            lecture.code,
            str(assignment.id),
            "edit",
            str(submission.id),
        )

        tmp_input_path = os.path.join(
            tmp_path,
            "input"
        )

        tmp_output_path = os.path.join(
            tmp_path,
            "output"
        )

        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path, ignore_errors=True)

        os.makedirs(tmp_input_path, exist_ok=True)

        # Init local repository
        command = "git init"
        await self._run_command_async(command, tmp_input_path)

        # Pull user repository
        command = f'git pull "{submission_repo_location}" main'
        await self._run_command_async(command, tmp_input_path)
        self.log.info("Successfully cloned repo")

        # Checkout to correct submission commit
        command = f"git checkout {submission.commit_hash}"
        await self._run_command_async(command, tmp_input_path)
        self.log.info(f"Now at commit {submission.commit_hash}")

        # Copy files to output directory
        shutil.copytree(tmp_input_path, tmp_output_path,
                        ignore=shutil.ignore_patterns(".git"))

        # Init local repository
        command = "git init"
        await self._run_command_async(command, tmp_output_path)

        # Add edit remote
        command = f"git remote add edit {edit_repo_location}"
        await self._run_command_async(command, tmp_output_path)
        self.log.info("Successfully added edit remote")

        # Switch to main
        command = "git switch -c main"
        await self._run_command_async(command, tmp_output_path)
        self.log.info("Successfully switched to branch main")

        # Add files to staging
        command = "git add -A"
        await self._run_command_async(command, tmp_output_path)
        self.log.info("Successfully added files to staging")

        # Commit Files
        command = 'git commit -m "Edit" --allow-empty'
        await self._run_command_async(command, tmp_output_path)
        self.log.info("Successfully committed files")

        # Push copied files
        command = "git push edit main --force"
        await self._run_command_async(command, tmp_output_path)
        self.log.info("Successfully pushed copied files")

        submission.edited = True
        self.session.commit()
        self.write_json(submission)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/submissions\/lti\/?",
    version_specifier=VersionSpecifier.ALL,
)
class LtiSyncHandler(GraderBaseHandler):
    cache_token = {"token": None, "ttl": datetime.datetime.now()}

    @authorize([Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        # build the subquery
        subquery = (self.session.query(Submission.username, func.max(Submission.date).label("max_date"))
                    .filter(Submission.assignid == assignment_id, Submission.feedback_status)
                    .group_by(Submission.username)
                    .subquery())

        # build the main query
        submissions: list[Submission] = (
            self.session.query(Submission)
            .join(subquery,
                  (Submission.username == subquery.c.username) & (Submission.date == subquery.c.max_date) & (
                          Submission.assignid == assignment_id) & Submission.feedback_status)
            .all())

        assignment: Assignment = self.get_assignment(lecture_id, assignment_id)
        lecture: Lecture = self.session.query(Lecture).get(lecture_id)

        lti_plugin = LTISyncGrades.instance()
        data = (lecture.serialize(), assignment.serialize(), [s.serialize() for s in submissions])

        if lti_plugin.check_if_lti_enabled(*data, sync_on_feedback=False):

            try:
                results = await lti_plugin.start(*data)
                self.write_json(results)
            except HTTPError as e:
                self.write_error(e.status_code, reason=e.reason)
                self.log.info("Could not sync grades: " + e.reason)
            except Exception as e:
                self.log.error("Could not sync grades: " + str(e))

        else:
            self.log.info("Skipping LTI plugin as it is not enabled")
            self.write_error(HTTPStatus.CONFLICT, reason="LTI Plugin is not enabled")
