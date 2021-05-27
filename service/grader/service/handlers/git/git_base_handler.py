import datetime
import calendar
import email.utils
import re
import subprocess
from grader.service.server import GraderServer
import tornado
from tornado.web import RequestHandler
import os
import logging

logger = logging.getLogger(__name__)

# TODO: probably change to super class to GraderBaseHandler for auth etc.
class GitBaseHandler(RequestHandler):
    def initialize(self, **kwargs):
        # set defaults
        self.gitcommand = "git"
        app: GraderServer = self.application
        self.gitbase = os.path.join(app.grader_service_dir, "git")

        self.cache_forever = lambda: [
            (
                "Expires",
                GitBaseHandler.get_date_header(
                    datetime.datetime.now() + datetime.timedelta(days=365)
                ),
            ),
            ("Pragma", "no-cache"),
            ("Cache-Control", "public, max-age=31556926"),
        ]

        self.dont_cache = lambda: [
            ("Expires", "Fri, 01 Jan 1980 00:00:00 GMT"),
            ("Pragma", "no-cache"),
            ("Cache-Control", "no-cache, max-age=0, must-revalidate"),
        ]

        self.file_headers = {
            re.compile(".*(/HEAD)$"): lambda: dict(
                self.dont_cache() + [("Content-Type", "text/plain")]
            ),
            re.compile(".*(/objects/info/alternates)$"): lambda: dict(
                self.dont_cache() + [("Content-Type", "text/plain")]
            ),
            re.compile(".*(/objects/info/http-alternates)$"): lambda: dict(
                self.dont_cache() + [("Content-Type", "text/plain")]
            ),
            re.compile(".*(/objects/info/packs)$"): lambda: dict(
                self.dont_cache() + [("Content-Type", "text/plain; charset=utf-8")]
            ),
            re.compile(".*(/objects/info/[^/]+)$"): lambda: dict(
                self.dont_cache() + [("Content-Type", "text/plain")]
            ),
            re.compile(".*(/objects/[0-9a-f]{2}/[0-9a-f]{38})$"): lambda: dict(
                self.cache_forever()
                + [("Content-Type", "application/x-git-loose-object")]
            ),
            re.compile(".*(/objects/pack/pack-[0-9a-f]{40}\\.pack)$"): lambda: dict(
                self.cache_forever()
                + [("Content-Type", "application/x-git-packed-objects")]
            ),
            re.compile(".*(/objects/pack/pack-[0-9a-f]{40}\\.idx)$"): lambda: dict(
                self.cache_forever()
                + [("Content-Type", "application/x-git-packed-objects-toc")]
            ),
        }

    @staticmethod
    def get_date_header(dt=None):
        if dt is None:
            dt = datetime.datetime.now()
        t = calendar.timegm(dt.utctimetuple())
        return email.utils.formatdate(t, localtime=False, usegmt=True)

    def gitlookup(self):
        pathlets = self.request.path.strip("/").split("/")
        # pathlets = ['services', 'grader', 'git', 'repo_name', ...]
        pathlets = pathlets[3:]
        path = os.path.abspath(os.path.join(self.gitbase, pathlets[0]))
        if not path.startswith(os.path.abspath(self.gitbase)):
            return None

        if os.path.exists(path):
            return path
        else:
            os.mkdir(path)
            # this path has to be a git dir -> call git init
            try:
                subprocess.run([self.gitcommand, "init", "--bare", path], check=True)
                subprocess.run(
                    [self.gitcommand, "update-server-info"],
                    cwd=path,
                    check=True,
                )
            except subprocess.CalledProcessError:
                return None
            return path

    def echo(self):
        print(self.request.path + "?" + self.request.query)
        body = self.request.body
        print("\t" + str(dict(self.request.headers.get_all())))
        if body == b"":
            body = "{}"
        print("\t" + str(tornado.escape.json_decode(body)))

    def get_gitdir(self):
        """Determine the git repository for this request"""
        gitdir = self.gitlookup()
        if gitdir is None:
            raise tornado.web.HTTPError(404, "unable to find repository")
        logger.debug("Accessing git at: %s", gitdir)

        return gitdir