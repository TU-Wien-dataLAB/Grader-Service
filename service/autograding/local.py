from re import S
from api.models import assignment
from orm.group import Group
from orm.lecture import Lecture
from orm.submission import Submission
from sqlalchemy.orm import Session
from traitlets.config.configurable import LoggingConfigurable
from dataclasses import dataclass
from datetime import datetime
from traitlets.traitlets import TraitError, Unicode, validate
import asyncio
import os
import shutil
import shlex
from tornado.process import Subprocess
from orm.assignment import Assignment


@dataclass
class AutogradingStatus:
    status: str
    started_at: datetime
    finished_at: datetime


class LocalAutogradeExecutor(LoggingConfigurable):

    base_input_path = Unicode(None, allow_none=False).tag(config=True)
    base_output_path = Unicode(None, allow_none=False).tag(config=True)

    convert_executable = Unicode("grader-convert", allow_none=False).tag(config=True)
    git_executable = Unicode("git", allow_none=False).tag(config=True)

    def __init__(self, grader_service_dir: str, submission: Submission, **kwargs):
        super().__init__(**kwargs)
        self.grader_service_dir = grader_service_dir
        self.submission = submission
        self.session: Session = Session.object_session(self.submission)

        self.autograding_start: datetime = None
        self.autograding_finished: datetime = None
        self.autograding_status: str = None
        self.autograde_result: asyncio.Future = None

    async def start(self):
        self._write_gradebook()
        await self._pull_submission()
        self.autograding_start = datetime.now()
        self.autograding_result = asyncio.ensure_future(self._run_autograde())
        await self.autograde_result
        self.autograding_finished = datetime.now()
        self._set_submission_properties()
        self._cleanup()

    @property
    def status(self) -> AutogradingStatus:
        if self.autograde_result is None:
            status = "not started"
        elif self.autograde_result.cancelled:
            status = "cancelled"
        else:
            status = "done" if self.autograde_result.done else "running"
        return AutogradingStatus(
            status, self.autograding_start, self.autograding_finished
        )

    @property
    def input_path(self):
        return os.path.join(self.base_input_path, f"submission_{self.submission.id}")

    @property
    def output_path(self):
        return os.path.join(self.base_output_path, f"submission_{self.submission.id}")

    def _write_gradebook(self):
        gradebook_str = self.submission.properties
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        path = os.path.join(self.output_path, "gradebook.json")
        self.log.info(f"Writing gradebook to {path}")
        with open(path, "w") as f:
            f.write(gradebook_str)

    async def _pull_submission(self):
        if not os.path.exists(self.input_path):
            os.mkdir(self.input_path)

        assignment: Assignment = self.submission.assignment
        lecture: Lecture = assignment.lecture

        if assignment.type == "user":
            repo_name = self.submission.username
        else:
            group = self.session.query(Group).get(
                (self.submission.username, lecture.id)
            )
            if group is None:
                raise ValueError()
            repo_name = group.name

        git_repo_path = os.path.join(
            self.grader_service_dir,
            "git",
            lecture.code,
            assignment.name,
            assignment.type,
            repo_name,
        )
        self.log.info(f"Cloning repo {git_repo_path} into input directory")
        command = f'{self.git_executable} clone "{git_repo_path}" "{self.input_path}"'
        process = Subprocess(shlex.split(command))
        await process.wait_for_exit()
        self.log.info("Successfully cloned repo")
        self.submission.auto_status = "pending"
        self.session.commit()

    async def _run_autograde(self):
        command = f'{self.convert_executable} autograde -i "{self.input_path}" -o "{self.output_path}" -p "*.ipynb"'
        self.log.info(f"Running {command}")
        process = Subprocess(shlex.split(command))
        await process.wait_for_exit()
        process_out = await process.stdout.read_until_close()
        self.log.info(process_out.decode("utf-8"))

    def _set_submission_properties(self):
        with open(os.path.join(self.output_path, "gradebook.json"), "r") as f:
            gradebook_str = f.read()
        self.submission.properties = gradebook_str
        self.submission.auto_status = "automatically_graded"
        self.session.commit()

    def _cleanup(self):
        shutil.rmtree(self.input_path)
        shutil.rmtree(self.output_path)

    @validate("base_input_path", "base_output_path")
    def _validate_service_dir(self, proposal):
        path: str = proposal["value"]
        if not os.path.isabs(path):
            raise TraitError("The path is not absolute")
        if not os.path.isdir(path):
            raise TraitError("The path has to be an existing directory")
        return path

    @validate("convert_executable", "git_executable")
    def _validate_executable(self, proposal):
        exec: str = proposal["value"]
        if shutil.which(exec) is None:
            raise TraitError(f"The executable is not valid: {exec}")
        return exec