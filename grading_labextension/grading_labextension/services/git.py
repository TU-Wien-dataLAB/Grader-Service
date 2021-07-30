import logging
import subprocess
from typing import List
from traitlets.config.configurable import Configurable
from traitlets.config.loader import Config
from traitlets.traitlets import Int, TraitError, Unicode, validate
import os
import posixpath
import shlex
from datetime import datetime
import getpass
import shutil
import sys

class GitError(Exception):
    def __init__(self, error: str):
        self.error = error
    
    def __str__(self):
        return self.error
    
    def __repr__(self) -> str:
        return self.__str__()

class GitService(Configurable):
    git_root_dir = Unicode(os.path.expanduser("~"), allow_none=False).tag(config=False) # is set by application
    git_access_token = Unicode(os.environ.get("JUPYTERHUB_API_TOKEN"), allow_none=False).tag(config=True)
    git_http_scheme = Unicode(os.environ.get("GRADER_HTTP_SCHEME", 'http'), allow_none=False).tag(config=True)
    git_remote_url = Unicode(f'{os.environ.get("GRADER_HOST_URL", "127.0.0.1")}:{os.environ.get("GRADER_HOST_PORT", "4010")}{os.environ.get("GRADER_GIT_BASE_URL", "/services/grader/git")}', allow_none=False).tag(config=True)

    def __init__(self, lecture_code: str, assignment_name: str, repo_type: str, force_user_repo=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._git_version = None
        self.lecture_code = lecture_code
        self.assignment_name = assignment_name
        self.repo_type = repo_type
        if self.repo_type in {"user", "group"} or force_user_repo:
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
        try:
            self._run_command(f"git remote add {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}", cwd=self.path)
        except GitError:
            self.log.info(f"Remote set: Updating remote {origin} for {self.path}")
            self._run_command(f"git remote set-url {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}", cwd=self.path)
        # self._run_command(f"git push --set-upstream {origin} main", cwd=self.path)
    
    def delete_remote(self, origin: str):
        raise NotImplementedError()

    def pull(self, origin: str, force=False):
        if force:
            self._run_command(f'sh -c "git clean -fd && git fetch --all && git reset --hard {origin}/main"',cwd=self.path)
            #self._run_command(f"git clean -fd", cwd=self.path)
            #self._run_command(f"git fetch --all", cwd=self.path)
            #self._run_command(f"git reset --hard {origin}/main", cwd=self.path)
        else:
            self._run_command(f"git pull {origin} main", cwd=self.path)

    def init(self, force=False):
        if not self.is_git() or force:
            self.log.info(f"Calling init for {self.path}")
            if self.git_version < (2,28):
                self._run_command(f"git init {self.path}")
                self._run_command("git checkout -b main", cwd=self.path)
            else:
                self._run_command(f"git init {self.path} -b main", cwd=self.path)
    
    def is_git(self):
        return os.path.exists(os.path.join(self.path, ".git"))
    

    def commit(self, m=str(datetime.now())):
        # self.log.info("Adding all files")
        # self._run_command(f'git add -A', cwd=self.path)
        # self.log.info("Committing repository")
        # self._run_command(f'git commit -m "{m}"', cwd=self.path)
        self.log.info("Adding all files and committing")
        self._run_command(f'sh -c "git add -A && git commit -m "{m}""', cwd=self.path)

    def set_author(self, author=getpass.getuser()):
        self._run_command(f'git config user.name "{author}"', cwd=self.path)
    
    def clone(self,origin: str, force=False):
        self.init(force=force)
        self.set_remote(origin=origin)
        self.pull(origin=origin,force=force)
    

    def delete_repo_contents(self):
        for root, dirs, files in os.walk(self.path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                if d != ".git":
                    shutil.rmtree(os.path.join(root, d))
    

    # ATTENTION: dirs_exist_ok was only added in Python 3.8
    def copy_repo_contents(self, src: str):
        ignore = shutil.ignore_patterns(".git", "__pycache__")
        if sys.version_info.major == 3 and sys.version_info.minor >= 8:
            shutil.copytree(src, self.path, ignore=ignore, dirs_exist_ok=True)
        else:
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(self.path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, ignore=ignore)
                else:
                    shutil.copy2(s, d)



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
            ret = subprocess.run(shlex.split(command), check=True, cwd=cwd, capture_output=True)
            if capture_output:
                return str(ret.stdout, 'utf-8')
        except subprocess.CalledProcessError as e:
            if capture_output:
                return None
            else:
                raise GitError(str(e.stdout, 'utf-8') + str(e.stderr, 'utf-8'))
        except FileNotFoundError as e:
            raise GitError(e.strerror)