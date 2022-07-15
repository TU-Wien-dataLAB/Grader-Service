## generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'
c.Spawner.cmd=["jupyter-labhub"]

## simple spawner
import os
config_dir = os.path.dirname(__file__)

c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'
c.Spawner.args = [f'--NotebookApp.config_file={os.path.join(config_dir, "jupyter_notebook_config.py")}']
c.SimpleLocalProcessSpawner.home_dir_template = os.path.join(config_dir, 'home_dir/{username}')

## dummy auth
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = "admin"
c.Authenticator.admin_users = {'user1'}
c.Authenticator.allowed_users = {"user1", "user2", "user3"}

## simple setup
c.JupyterHub.ip = '127.0.0.1'
c.JupyterHub.port = 8080

c.JupyterHub.services.append(
    {
        'name': 'grader',
        'url': 'http://127.0.0.1:4010',
        'api_token': '7572f93a2e7640999427d9289c8318c0'
    }
)

c.JupyterHub.load_groups = {
        "20wle2:instructor": ["user1", "user2"],
        "20wle2:student": ["user3"],
        "22wle1:instructor": ["user1", "user2"],
        "22wle1:student": ["user3"],
}

c.JupyterHub.log_level = "INFO"
