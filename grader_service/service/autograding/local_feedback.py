import json
import os
import shutil
from subprocess import CalledProcessError
from .local_grader import LocalAutogradeExecutor, rm_error
from grader_convert.gradebook.models import GradeBookModel
from ..orm.assignment import Assignment
from ..orm.group import Group
from ..orm.lecture import Lecture
from ..orm.submission import Submission
from grader_convert.converters.generate_feedback import GenerateFeedback


class GenerateFeedbackExecutor(LocalAutogradeExecutor):
    def __init__(self, grader_service_dir: str, submission: Submission, **kwargs):
        super().__init__(grader_service_dir, submission, **kwargs)

    @property
    def input_path(self):
        return os.path.join(self.base_input_path, f"feedback_{self.submission.id}")

    @property
    def output_path(self):
        return os.path.join(self.base_output_path, f"feedback_{self.submission.id}")

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
            "autograde",
            assignment.type,
            repo_name,
        )

        if os.path.exists(self.input_path):
            shutil.rmtree(self.input_path, onerror=rm_error)
        os.mkdir(self.input_path)

        self.log.info(f"Pulling repo {git_repo_path} into input directory")

        command = f"{self.git_executable} init"
        self.log.info(f"Running {command}")
        try:
            await self._run_subprocess(command, self.input_path)
        except CalledProcessError:
            pass

        command = f'{self.git_executable} pull "{git_repo_path}"  submission_{self.submission.commit_hash}'
        self.log.info(f"Running {command}")
        try:
            await self._run_subprocess(command, self.input_path)
        except CalledProcessError:
            pass
        self.log.info("Successfully cloned repo")

    def _write_gradebook(self):
        gradebook_str = self.submission.properties
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        path = os.path.join(self.output_path, "gradebook.json")
        self.log.info(f"Writing gradebook to {path}")
        with open(path, "w") as f:
            f.write(gradebook_str)

    async def _run(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path, onerror=rm_error)

        os.mkdir(self.output_path)
        self._write_gradebook()

        # command = f'{self.convert_executable} generate_feedback -i "{self.input_path}" -o "{self.output_path}" -p "*.ipynb"'
        # self.log.info(f"Running {command}")
        # try:
        #     process = await self._run_subprocess(command, None)
        # except CalledProcessError:
        #     raise # TODO: exit gracefully
        # output = process.stderr.read().decode("utf-8")
        # self.log.info(output)
        autograder = GenerateFeedback(self.input_path, self.output_path, "*.ipynb")
        autograder.force = True
        autograder.start()

    async def _push_results(self):
        os.unlink(os.path.join(self.output_path, "gradebook.json"))

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
            "feedback",
            assignment.type,
            repo_name,
        )

        if not os.path.exists(git_repo_path):
            os.makedirs(git_repo_path, exist_ok=True)
            try:
                await self._run_subprocess(
                    f'git init --bare "{git_repo_path}"', self.output_path
                )
            except CalledProcessError:
                raise

        command = f"{self.git_executable} init"
        self.log.info(f"Running {command} at {self.output_path}")
        try:
            await self._run_subprocess(command, self.output_path)
        except CalledProcessError:
            pass

        self.log.info(f"Creating new branch feedback_{self.submission.commit_hash}")
        command = (
            f"{self.git_executable} switch -c feedback_{self.submission.commit_hash}"
        )
        try:
            await self._run_subprocess(command, self.output_path)
        except CalledProcessError:
            pass
        self.log.info(f"Now at branch feedback_{self.submission.commit_hash}")

        self.log.info(f"Commiting all files in {self.output_path}")
        try:
            await self._run_subprocess(
                f"{self.git_executable} add -A", self.output_path
            )
            await self._run_subprocess(
                f'{self.git_executable} commit -m "{self.submission.commit_hash}"',
                self.output_path,
            )
        except CalledProcessError:
            pass  # TODO: exit gracefully

        self.log.info(
            f"Pushing to {git_repo_path} at branch feedback_{self.submission.commit_hash}"
        )
        command = f'{self.git_executable} push -uf "{git_repo_path}" feedback_{self.submission.commit_hash}'
        try:
            await self._run_subprocess(command, self.output_path)
        except CalledProcessError:
            pass  # TODO: exit gracefully
        self.log.info("Pushing complete")

    def _set_properties(self):
        with open(os.path.join(self.output_path, "gradebook.json"), "r") as f:
            gradebook_str = f.read()
        gradebook_dict = json.loads(gradebook_str)
        book = GradeBookModel.from_dict(gradebook_dict)
        score = 0
        for id, n in book.notebooks.items():
            score += n.score
        self.submission.score = score
        self.session.commit()

    def _set_db_state(self):
        self.submission.feedback_available = True
        self.session.commit()
