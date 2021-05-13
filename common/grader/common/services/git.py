from traitlets.config.configurable import SingletonConfigurable
from traitlets.traitlets import Int, TraitError, Unicode, validate


class GitService(SingletonConfigurable):
    git_local_root_dir = Unicode(None, allow_none=False).tag(config=False) # is set by application
    git_access_token = Unicode('', allow_none=False).tag(config=True)
    git_remote_url = Unicode('', allow_none=False).tag(config=True)

    def push(self, force=False):
        raise NotImplementedError()

    def fetch(self, force=False):
        raise NotImplementedError()

    def get_lecture_repository(lecture_name: str, semester: str):
        raise NotImplementedError()