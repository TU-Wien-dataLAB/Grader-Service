import subprocess
from traitlets.config.configurable import Configurable
from traitlets.traitlets import Int, TraitError, Unicode, validate
import os
import posixpath
import shlex

class GitError(Exception):
    pass

class GitService(Configurable):
    git_root_dir = Unicode(os.path.expanduser("~"), allow_none=False).tag(config=False) # is set by application
    git_access_token = Unicode('', allow_none=False).tag(config=True)
    git_http_scheme = Unicode('http', allow_none=False).tag(config=True)
    git_remote_url = Unicode('', allow_none=False).tag(config=True)

    def __init__(self, lecture_code: str, assignment_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lecture_code = lecture_code
        self.assignment_name = assignment_name
        self.path = os.path.join(self.git_root_dir, self.lecture_code, self.assignment_name)
        

    def push(self, name: str, force=False):
        self._run_command(f"git push {name} main" + (" --force" if force else ""), cwd=self.path)
    
    def set_remote(self, name: str):
        url = posixpath.join(self.git_remote_url, self.lecture_code, self.assignment_name)
        self._run_command(f"git remote add {name} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}")
        self._run_command(f"git push --set-upstream {name} main")
    
    def delete_remote(self, name: str):
        raise NotImplementedError()

    def pull(self, name: str, force=False):
        self._run_command(f"git pull {name} main" + (" --force" if force else ""), cwd=self.path)

    def init(self, force=False):
        if not os.path.exists(os.path.join(self.path, ".git")) or force:
            self._run_command(f"git init {self.path}")
    
    def clone():
        raise NotImplementedError()
    
    def _run_command(self, command, cwd=None):
        try:
            subprocess.run(shlex.split(command), check=True, cwd=cwd)
        except subprocess.CalledProcessError:
            raise GitError