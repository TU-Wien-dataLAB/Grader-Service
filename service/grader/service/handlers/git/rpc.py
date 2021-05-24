from grader.common.registry import register_handler
from grader.service.handlers.git.git_base_handler import GitBaseHandler
from grader.service.handlers.git.iowrapper import ProcessWrapper


@register_handler(path="/.*/git-.*")
class GitRPCHandler(GitBaseHandler):
    """Request handler for RPC calls

    Use this handler to handle example.git/git-upload-pack and example.git/git-receive-pack URLs"""

    async def post(self):
        self.echo()
        gitdir = self.get_gitdir()

        # get RPC command
        pathlets = self.request.path.strip("/").split("/")
        rpc = pathlets[-1]
        rpc = rpc[4:]

        p = ProcessWrapper(
            self,
            [self.gitcommand, rpc, "--stateless-rpc", gitdir],
            {"Content-Type": "application/x-git-%s-result" % rpc},
        )
        await p.finish_state
