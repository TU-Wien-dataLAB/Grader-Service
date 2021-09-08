from autograding.local import LocalAutogradeExecutor
from registry import VersionSpecifier, register_handler
from handlers.base_handler import GraderBaseHandler, authorize
from jupyter_server.utils import url_path_join
from orm.takepart import Scope
from orm.submission import Submission


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
    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, sub_id: int):
        submission = self.session.query(Submission).get(sub_id)
        executor = LocalAutogradeExecutor(self.application.grader_service_dir, submission)
        executor.start()
        self.session.commit()
        submission = self.session.query(Submission).get(sub_id)
        self.write_json(submission)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/manual\/?",
    version_specifier=VersionSpecifier.ALL,
)
class GradingManualHandler(GraderBaseHandler):
    @authorize([Scope.tutor, Scope.instructor])
    async def post(self, lecture_id: int, assignment_id: int, user_id: int):
        pass

    @authorize([Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, user_id: int):
        pass

    @authorize([Scope.tutor, Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int, user_id: int):
        pass

    @authorize([Scope.instructor])
    async def delete(self, lecture_id: int, assignment_id: int, user_id: int):
        pass


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/grading\/(?P<user_id>\d*)\/score\/?",
    version_specifier=VersionSpecifier.ALL,
)
class GradingScoreHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, user_id: int):
        pass
