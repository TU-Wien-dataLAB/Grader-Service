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
        if self.gitcommand is None:
            self.gitcommand = 'git'
        app: GraderServer = self.application
        self.gitbase = os.path.join(app.grader_service_dir, "git")
    
    def gitlookup(self):
        pathlets = self.request.path.strip('/').split('/')

        path = os.path.abspath(os.path.join(self.gitbase, pathlets[0]))
        if not path.startswith(os.path.abspath(self.gitbase)):
            return None

        if os.path.exists(path):
            return path
    
    def get_gitdir(self):
        """Determine the git repository for this request"""
        if self.gitlookup is None:
            raise tornado.web.HTTPError(500, 'no git lookup configured')

        gitdir = self.gitlookup(self.request)
        if gitdir is None:
            raise tornado.web.HTTPError(404, 'unable to find repository')
        logger.debug("Accessing git at: %s", gitdir)

        return gitdir