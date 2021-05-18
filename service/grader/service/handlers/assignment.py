from grader.common.models.error_message import ErrorMessage
from grader.common.registry import register_handler
from grader.common.services.compression import CompressionEngine
from grader.common.services.git import GitService
from grader.service.handlers.base_handler import GraderBaseHandler, authenticated
from grader.service.main import GraderService
from grader.service.orm import lecture
from grader.service.orm import assignment
from grader.service.orm.assignment import Assignment
from grader.service.orm.file import File
from grader.service.orm.lecture import Lecture
from grader.service.orm.takepart import Role, Scope
import os.path as osp
from grader.service.server import GraderServer
from jupyter_server.utils import url_path_join
from grader.common.models.assignment import Assignment as AssignmentModel
from grader.service.persistence.assignment import get_assignments
from sqlalchemy.sql.expression import false, join
from tornado import httputil
import tornado


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(GraderBaseHandler):
    @authenticated
    def get(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(403, ErrorMessage("Unautorized!"))
            return

        self.write(role.lecture.assignments)

    @authenticated
    def post(self, lecture_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None or role.role < Scope.instructor:
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return

        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = Assignment()

        assignment.name = assignment_model.name
        assignment.lectid = lecture_id
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status
        self.session.add(assignment)
        self.session.commit()
        self.write(assignment)


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(GraderBaseHandler):
    @authenticated
    def put(self, lecture_id: int, assignment_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None or role.role < Scope.instructor:
            self.write_error(403, ErrorMessage("Unauthorized!"))
            return

        body = tornado.escape.json_decode(self.request.body)
        assignment_model = AssignmentModel.from_dict(body)
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return

        assignment.name = assignment_model.name
        assignment.duedate = assignment_model.due_date
        assignment.status = assignment_model.status

    @authenticated
    def get(self, lecture_id: int, assignment_id: int):
        instructor_version = self.get_argument("instructor-version", False)
        metadata_only = self.get_argument("metadata-only", False)
        
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(403, ErrorMessage("Unautorized!"))
            return
        assignment = self.session.query(Assignment).get(assignment_id)
        if assignment is None:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        self.write(assignment)

    @authenticated
    def delete(self, lecture_id: int, assignment_id: int):
        pass  # TODO: set delete action in database


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

    @authenticated
    def get(self, lecture_id: int, assignment_id: int, file_id: int):
        role = self.session.query(Role).get((self.user.name, lecture_id))
        if role is None:
            self.write_error(403, ErrorMessage("Unautorized!"))
            return
        file = self.session.query(File).get(file_id)
        if file is None or file.assignid != assignment_id:
            self.write_error(404, ErrorMessage("Not Found!"))
            return
        assignment: Assignment = file.assignment
        lectrue: Lecture = assignment.lecture
        path = osp.join(lectrue.name, assignment.name, file.path)
        full_path = osp.join(GitService.instance().git_local_root_dir, path)

        archive_file = self.compression_engine.create_archive(name=f"{lectrue.name}_{assignment.name}_{file.path}", path=full_path)
        with open(archive_file, "rb") as f:
            data = f.read()
            self.write(data)
