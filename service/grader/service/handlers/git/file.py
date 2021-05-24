from grader.common.registry import register_handler
from grader.service.handlers.git.git_base_handler import GitBaseHandler
import tornado
import os
import json
from grader.service.handlers.git.iowrapper import FileWrapper

@register_handler(path='/.*/objects/.*')
class GitFileHandler(GitBaseHandler):
    """Request handler for static files"""

    async def get(self):
        self.echo()

        gitdir = self.get_gitdir()
        # determine the headers for this file
        filename, headers = None, None
        for matcher, get_headers in self.file_headers.items():
            m = matcher.match(self.request.path)
            if m:
                filename = m.group(1)
                headers = get_headers()
                break
        
        if not filename:
            raise tornado.web.HTTPError(404, 'File not Found!')
        
        # expand filename
        filename = os.path.abspath(os.path.join(gitdir, filename.lstrip('/')))
        if not filename.startswith(os.path.abspath(gitdir)): # yes, the matches are strict and don't allow directory traversal, but better safe than sorry
            raise tornado.web.HTTPError(404, 'Trying to access file outside of git repository')
        
        FileWrapper(self, filename, headers)



@register_handler(path='/.*/HEAD')
class GitHeadHandler(GitFileHandler):
    pass # only for different path