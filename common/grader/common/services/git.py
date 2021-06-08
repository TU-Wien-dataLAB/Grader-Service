import subprocess
from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Int, TraitError, Unicode, validate
import os
import posixpath
import shlex

class GitError(Exception):
    pass

class GitService(SingletonConfigurable):
    git_root_dir = Unicode(os.path.expanduser("~"), allow_none=False).tag(config=False) # is set by application
    git_access_token = Unicode('', allow_none=False).tag(config=True)
    git_http_scheme = Unicode('http', allow_none=False).tag(config=True)
    git_remote_url = Unicode('', allow_none=False).tag(config=True)

    def push(self, name: str, lecture_code: str, assignment_name: str, force=False):
        path = os.path.join(self.git_root_dir, lecture_code, assignment_name)
        self._run_command(f"git push {name} main" + (" --force" if force else ""), cwd=path)
    
    def set_remote(self, name: str, lecture_code: str, assignment_name: str):
        url = posixpath.join(self.git_remote_url, lecture_code, assignment_name)
        self._run_command(f"git remote add {name} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}")
        self._run_command(f"git push --set-upstream {name} main")

    def pull(self, name: str, lecture_code: str, assignment_name: str, force=False):
        path = os.path.join(self.git_root_dir, lecture_code, assignment_name)
        self._run_command(f"git pull {name} main" + (" --force" if force else ""), cwd=path)

    def init(self, lecture_code: str, assignment_name: str, force=False):
        path = os.path.join(self.git_root_dir, lecture_code, assignment_name)
        if not os.path.exists(path) or force:
            self._run_command(f"git init {path}")
            self.set_remote("grader", lecture_code, assignment_name)
    
    def _run_command(command, cwd=None):
        try:
            subprocess.run(shlex.split(command), check=True, cwd=cwd)
        except subprocess.CalledProcessError:
            raise GitError