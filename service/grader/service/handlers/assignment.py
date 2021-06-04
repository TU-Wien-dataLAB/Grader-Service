from grader.common.models.assignment_file import AssignmentFile
from grader.common.models.error_message import ErrorMessage
from grader.common.models.exercise import Exercise
from grader.common.registry import register_handler
from grader.common.services.compression import CompressionEngine
from grader.common.services.git import GitService
from grader.service.handlers.base_handler import GraderBaseHandler, authorize
from grader.service.main import GraderService
from grader.service.orm import lecture
from grader.service.orm import assignment
from grader.service.orm.assignment import Assignment
from grader.service.orm.base import DeleteState
from grader.service.orm.file import File
from grader.service.orm.lecture import Lecture
from grader.service.orm.takepart import Role, Scope
import os.path as osp
from grader.service.server import GraderServer
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment as AssignmentModel
from sqlalchemy.sql.expression import false, join
from sqlalchemy.orm.exc import ObjectDeletedError
from tornado import httputil
import tornado
from tornado.web import HTTPError


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(GraderBaseHandler):
    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role.lecture.deleted == DeleteState.deleted:
            self.error_message = "Not Found"
            raise HTTPError(404)
        
        assignments = [a for a in role.lecture.assignments if a.deleted == DeleteState.active]
        self.write_json(assignments)

    @authorize([Scope.instructor])
    async def post(self, lecture_id: int):
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = Assignment()

        if len(set([e.path for e in assignment_model.exercises] + [f.path for f in assignment_model.files])) != len(assignment_model.exercises + assignment_model.files):
            self.error_message = "Some files share the same name"
            raise HTTPError(400)

        assignment.name = assignment_model.name
        assignment.lectid = lecture_id
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status
        assignment.points = sum([ex.points for ex in assignment_model.exercises])
        assignment.deleted = DeleteState.active
        self.session.add(assignment)
        self.session.commit()

        ex: Exercise
        for ex in assignment_model.exercises:
            file = File()
            file.assignid = assignment.id
            file.exercise = True
            file.name = ex.name
            file.path = ex.path
            file.points = ex.points
            self.session.add(file)
        
        f: AssignmentFile
        for f in assignment_model.files:
            file = File()
            file.assignid = assignment.id
            file.exercise = False
            file.name = f.name
            file.path = f.path
            file.points = None
            self.session.add(file)

        self.session.commit()
        self.write_json(assignment)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(GraderBaseHandler):
    @authorize([Scope.instructor])
    async def put(self, lecture_id: int, assignment_id: int):
        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)

        assignment.name = assignment_model.name
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int):
        instructor_version = self.get_argument("instructor-version", False)
        metadata_only = self.get_argument("metadata-only", False)
        
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if instructor_version and role.role < Scope.instructor:
            raise HTTPError(403)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None or assignment.deleted == DeleteState.deleted:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        self.write_json(assignment)

    @authorize([Scope.instructor])
    async def delete(self, lecture_id: int, assignment_id: int):
        try:
            assignment = self.session.query(Assignment).get(assignment_id)
            if assignment is None:
                raise HTTPError(404)
            assignment.deleted = 1
            if assignment.deleted == 1:
                raise HTTPError(404)
        except ObjectDeletedError:
            raise HTTPError(404)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/file\/(?P<file_id>\d*)\/?"
)
class AssignmentDataHandler(GraderBaseHandler):
    def __init__(
        self, application: GraderServer, request: httputil.HTTPServerRequest, **kwargs
    ) -> None:
        super().__init__(application, request, **kwargs)
        app: GraderServer = self.application
        self.compression_engine = CompressionEngine(
            compression_dir=osp.join(app.grader_service_dir, "archive")
        )

    @authorize([Scope.student, Scope.tutor, Scope.instructor])
    async def get(self, lecture_id: int, assignment_id: int, file_id: int):
        file = self.session.query(File).get(file_id)
        if file is None or file.assignid != assignment_id:
            self.error_message = "Not Found!"
            raise HTTPError(404)
        assignment: Assignment = file.assignment
        lectrue: Lecture = assignment.lecture
        path = osp.join(lectrue.name, assignment.name, file.path)
        full_path = osp.join(GitService.instance().git_local_root_dir, path)

        archive_file = self.compression_engine.create_archive(name=f"{lectrue.name}_{assignment.name}_{file.path}", path=full_path)
        with open(archive_file, "rb") as f:
            data = f.read()
            self.write_json(data)
