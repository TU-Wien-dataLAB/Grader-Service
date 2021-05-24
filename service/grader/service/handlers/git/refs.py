from grader.common.registry import register_handler
from grader.service.handlers.git.git_base_handler import GitBaseHandler
import tornado
from urllib.parse import parse_qs
import os
from grader.service.handlers.git.iowrapper import FileWrapper, ProcessWrapper


@register_handler(path="/.*/info/refs")
class GitInfoRefsHandler(GitBaseHandler):
    """Request handler for info/refs

    Use this handler to handle example.git/info/refs?service= URLs"""

    async def get(self):
        self.echo()

        gitdir = self.get_gitdir()
        rpc: str = parse_qs(self.request.query).get("service", [""])[0]
        if not rpc:
            # this appears to be a dumb client. send the file
            FileWrapper(
                self,
                os.path.join(gitdir, "info", "refs"),
                dict(
                    self.dont_cache() + [("Content-Type", "text/plain; charset=utf-8")]
                ),
            )
            return

        rpc = rpc[4:]  # remove 'git-'
        prelude: str = "# service=git-" + rpc
        prelude = str(hex(len(prelude) + 4)[2:].rjust(4, "0")) + prelude
        prelude += "0000"  # packet flush

        p = ProcessWrapper(
            self,
            [self.gitcommand, rpc, "--stateless-rpc", "--advertise-refs", gitdir],
            {
                "Content-Type": "application/x-git-%s-advertisement" % rpc,
                "Expires": "Fri, 01 Jan 1980 00:00:00 GMT",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache, max-age=0, must-revalidate",
            },
            prelude,
        )
        await p.finish_state
