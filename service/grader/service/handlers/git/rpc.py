from grader.common.registry import register_handler
from grader.service.handlers.git.git_base_handler import GitBaseHandler
import tornado

@register_handler(path='/.*/git-.*')
class GitRPCHandler(GitBaseHandler):

    def echo(self: GitBaseHandler):
        print(self.request.path)
        body = self.request.body
        if body == b'':
            body = "{}"
        print(tornado.escape.json_decode(body))

    def get(self):
        self.echo()
    def post(self):
        self.echo()
    def put(self):
        self.echo()
    def delete(self):
        self.echo()

