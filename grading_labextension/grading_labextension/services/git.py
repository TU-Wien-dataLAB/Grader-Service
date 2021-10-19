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
from urllib.parse import quote

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
        self.log = logging.getLogger(str(self.__class__))
        self._git_version = None
        self.lecture_code = lecture_code
        self.assignment_name = assignment_name
        self.repo_type = repo_type
        if self.repo_type == "assignment" or force_user_repo:
            self.path = os.path.join(self.git_root_dir, self.lecture_code, self.assignment_name)
        else:
            self.path = os.path.join(self.git_root_dir, self.repo_type, self.lecture_code, self.assignment_name)
        self.log.info(f"New git service working in {self.path}")
        os.makedirs(self.path, exist_ok=True)

        self.log.info("git_access_token: " + self.git_access_token)
        self.log.info("git_http_scheme: " + self.git_http_scheme)
        self.log.info("git_remote_url: " + self.git_remote_url)        


    def push(self, origin: str, force=False):
        """Pushes commits on the remote

        Args:
            origin (str): the remote
            force (bool, optional): states if the operation should be forced. Defaults to False.
        """
        self.log.info(f"Pushing remote {origin} for {self.path}")
        self._run_command(f"git push {origin} main" + (" --force" if force else ""), cwd=self.path)
    
    def set_remote(self, origin: str, sub_id=None):
        """Set a remote in the local repository

        Args:
            origin (str): the remote
            sub_id ([type], optional): a query param for the feedback pull. Defaults to None.
        """
        self.log.info(f"Setting remote {origin} for {self.path}")
        url = posixpath.join(self.git_remote_url, self.lecture_code, quote(self.assignment_name), self.repo_type)
        try:
            if sub_id is None:
                self._run_command(f"git remote add {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}", cwd=self.path)
            else:
                self.log.info(f"Setting remote with sub_id {sub_id}")
                self._run_command(f"git remote add {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{posixpath.join(url, sub_id)}", cwd=self.path)

        except GitError as e:
            self.log.error("GitError:\n" + e.error)
            self.log.info(f"Remote set: Updating remote {origin} for {self.path}")
            if sub_id is None:
                self._run_command(f"git remote set-url {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{url}", cwd=self.path)
            else:
                self.log.info(f"Setting remote with sub_id {sub_id}")
                self._run_command(f"git remote set-url {origin} {self.git_http_scheme}://oauth:{self.git_access_token}@{posixpath.join(url, sub_id)}", cwd=self.path)

    def delete_remote(self, origin: str):
        raise NotImplementedError()

    def switch_branch(self,branch: str):
        """Switches into another branch

        Args:
            branch (str): the branch name
        """
        self.log.info(f"Fetching all at path {self.path}")
        self._run_command(f"git fetch --all", cwd=self.path)
        self.log.info(f"Switching to branch {branch} at path {self.path}")
        self._run_command(f"git checkout {branch}", cwd=self.path)

    def pull(self, origin: str, branch="main", force=False):
        """Pulls a repository

        Args:
            origin (str): the remote
            branch (str, optional): the branch name. Defaults to "main".
            force (bool, optional): states if the operation should be forced. Defaults to False.
        """
        if force:
            self.log.info(f"Pulling remote {origin}")
            out = self._run_command(f'sh -c "git clean -fd && git fetch {origin} && git reset --hard {origin}/{branch}"', cwd=self.path, capture_output=True)
            self.log.info(out)
            #self._run_command(f'sh -c "git fetch --all && git reset --mixed {origin}/main"',cwd=self.path)
        else:
            self._run_command(f"git pull {origin} {branch}", cwd=self.path)

    def init(self, force=False):
        """Initiates a local repository

        Args:
            force (bool, optional): states if the operation should be forced. Defaults to False.
        """
        if not self.is_git() or force:
            self.log.info(f"Calling init for {self.path}")
            if self.git_version < (2,28):
                self._run_command(f"git init", cwd=self.path)
                self._run_command("git checkout -b main", cwd=self.path)
            else:
                self._run_command(f"git init -b main", cwd=self.path)
    
    def is_git(self):
        """Checks if the directory is a local repository

        Returns:
            bool: states if the directory is a repository
        """
        return os.path.exists(os.path.join(self.path, ".git"))
    

    def commit(self, m=str(datetime.now())):
        """Commits the staged changes

        Args:
            m (str, optional): the commit message. Defaults to str(datetime.now()).
        """
        # self.log.info("Adding all files")
        # self._run_command(f'git add -A', cwd=self.path)
        # self.log.info("Committing repository")
        # self._run_command(f'git commit -m "{m}"', cwd=self.path)
        self.log.info(f"Adding all files and committing in {self.path}")
        self._run_command(f'sh -c "git add -A && git commit --allow-empty -m "{m}""', cwd=self.path)

    def set_author(self, author=getpass.getuser()):
        self._run_command(f'git config user.name "{author}"', cwd=self.path)
    
    def clone(self,origin: str, force=False):
        """Clones the repository

        Args:
            origin (str): the remote
            force (bool, optional): states if the operation should be forced. Defaults to False.
        """
        self.init(force=force)
        self.set_remote(origin=origin)
        self.pull(origin=origin,force=force)
    

    def delete_repo_contents(self, include_git=False):
        """Deletes the contents of the git service

        Args:
            include_git (bool, optional): states if the .git directory should also be deleted. Defaults to False.
        """
        for root, dirs, files in os.walk(self.path):
            for f in files:
                os.unlink(os.path.join(root, f))
                self.log.info(f"Deleted {os.path.join(root, f)} from {self.git_root_dir}")
            for d in dirs:
                if d != ".git" or include_git:
                    shutil.rmtree(os.path.join(root, d))
                    self.log.info(f"Deleted {os.path.join(root, d)} from {self.git_root_dir}")
    

    # ATTENTION: dirs_exist_ok was only added in Python 3.8
    def copy_repo_contents(self, src: str):
        """copies repo contents from src to the git path

        Args:
            src (str): path where the to be copied files reside
        """
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
        """Return the git version

        Returns:
            tuple: the git version
        """
        if self._git_version is None:
            try:
                version = self._run_command("git --version", capture_output=True)
            except GitError:
                return tuple()
            version = version.split(" ")[2]
            self._git_version = tuple([int(v) for v in version.split(".")])
        return self._git_version
    
    def _run_command(self, command, cwd=None, capture_output=False):
        """Starts a sub process and runs an cmd command

        Args:
            command str: command that is getting run.
            cwd (str, optional): states where the command is getting run. Defaults to None.
            capture_output (bool, optional): states if output is getting saved. Defaults to False.

        Raises:
            GitError: returns appropriate git error 

        Returns:
            str: command output
        """
        try:
            self.log.info(f"Running: {command}")
            ret = subprocess.run(shlex.split(command), check=True, cwd=cwd, capture_output=True)
            if capture_output:
                return str(ret.stdout, 'utf-8')
        except subprocess.CalledProcessError as e:
            raise GitError(str(e.stdout, 'utf-8') + str(e.stderr, 'utf-8'))
        except FileNotFoundError as e:
            raise GitError(e.strerror)