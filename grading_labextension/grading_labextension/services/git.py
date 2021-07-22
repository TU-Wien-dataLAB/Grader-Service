import logging
import subprocess
from traitlets.config.configurable import Configurable
from traitlets.config.loader import Config
from traitlets.traitlets import Int, TraitError, Unicode, validate
import os
import posixpath
import shlex
from datetime import datetime
import getpass

class GitError(Exception):
    pass

class GitService(Configurable):
    git_root_dir = Unicode(os.path.expanduser("~"), allow_none=False).tag(config=False) # is set by application
    git_access_token = Unicode(None, allow_none=False).tag(config=True)
    git_http_scheme = Unicode('http', allow_none=False).tag(config=True)
    git_remote_url = Unicode(None, allow_none=False).tag(config=True)

    def __init__(self, lecture_code: str, assignment_name: str, repo_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._git_version = None
        self.lecture_code = lecture_code
        self.assignment_name = assignment_name
        self.repo_type = repo_type
        if self.repo_type in {"user", "group"}:
            self.path = os.path.join(self.git_root_dir, self.lecture_code, self.assignment_name)
        else:
            self.path = os.path.join(self.git_root_dir, self.repo_type, self.lecture_code, self.assignment_name)
        os.makedirs(self.path, exist_ok=True)

        self.log = logging.getLogger(str(self.__class__))
        self.log.info("git_access_token: " + self.git_access_token)
        self.log.info("git_http_scheme: " + self.git_http_scheme)
        self.log.info("git_remote_url: " + self.git_remote_url)        


    def push(self, origin: str, force=False):
        self.log.info(f"Pushing remote {origin} for {self.path}")
        self._run_command(f"git push {origin} main" + (" --force" if force else ""), cwd=self.path)
    
    def set_remote(self, origin: str):
        self.log.info(f"Setting remote {origin} for {self.path}")
        url = posixpath.join(self.git_remote_url, self.lecture_code, self.assignment_name, self.repo_type)
        self._run_command(f"git remote add {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}", cwd=self.path)
        self._run_command(f"git push --set-upstream {origin} main", cwd=self.path)
    
    def delete_remote(self, origin: str):
        raise NotImplementedError()

    def pull(self, origin: str, force=False):
        self._run_command(f"git pull {origin} main" + (" --force" if force else ""), cwd=self.path)

    def init(self, force=False):
        if not self.is_git() or force:
            self.log.info(f"Calling init for {self.path}")
            if self.git_version < (2,28):
                self._run_command(f"git init {self.path}")
                self._run_command("git checkout -b main")
            else:
                self._run_command(f"git init {self.path} -b main")
    
    def is_git(self):
        return os.path.exists(os.path.join(self.path, ".git"))
    

    def commit(self, m=str(datetime.now())):
        self.log.info("Committing repository")
        self._run_command(f'git add -A', cwd=self.path)
        self._run_command(f'git commit -m "{m}"', cwd=self.path)

    def set_author(self, author=getpass.getuser()):
        self._run_command(f'git config user.name "{author}"', cwd=self.path)
    
    def clone():
        raise NotImplementedError()

    @property
    def git_version(self):
        if self._git_version is None:
            version = self._run_command("git --version", capture_output=True)
            if version is None:
                return tuple()
            version = version.split(" ")[2]
            self._git_version = tuple([int(v) for v in version.split(".")])
        return self._git_version
    
    def _run_command(self, command, cwd=None, capture_output=False):
        try:
            ret = subprocess.run(shlex.split(command), check=True, cwd=cwd, capture_output=capture_output)
            if capture_output:
                return str(ret.stdout, 'utf-8')
        except subprocess.CalledProcessError:
            if capture_output:
                return None
            else:
                raise GitError