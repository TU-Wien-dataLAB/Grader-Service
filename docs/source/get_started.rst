Get Started
**************

Running grader service
=======================

To run the grader service you first have to register the service in JupyterHub as an unmanaged service in the config: ::

    c.JupyterHub.services.append(
        {
            'name': 'grader',
            'url': 'http://127.0.0.1:4010',
            'api_token': '<token>'
        }
    )


You can verify the config by running ``jupyterhub -f <config_file.py>`` and you should see the following error message: ::

    Cannot connect to external service grader at http://127.0.0.1:4010. Is it running?

Specifying user roles
======================

Since the JupyterHub is the only source of authentication for the service, it has to rely on the JupyterHub to provide all the necessary information for user groups.

Users have to be added to specific groups which maps the users to lectures and roles. They have to be separated by colons.

The config could look like this: ::

    c.JupyterHub.load_groups = {
        "lect1:instructor": ["user1"],
        "lect1:tutor": ["user2"],
        "lect1:student": ["user3", "user4"]
    }

Here, ``user1`` is an instructor of the lecture with the code ``lect1`` and so on.

Starting the service
=====================

In order to start the grader service we have to provide a configuration file for it as well: ::

    import os

    c.GraderService.service_host = "127.0.0.1"
    # existing directory to use as the base directory for the grader service
    service_dir = os.path.expanduser("<grader_service_dir>")
    c.GraderService.grader_service_dir = service_dir

    c.GraderServer.hub_service_name = "grader"
    c.GraderServer.hub_api_token = "<token>"
    c.GraderServer.hub_api_url = "http://127.0.0.1:8081/hub/api"
    c.GraderServer.hub_base_url = "/"

    c.LocalAutogradeExecutor.base_input_path = os.path.expanduser(os.path.join(service_dir, "convert_in"))
    c.LocalAutogradeExecutor.base_output_path = os.path.expanduser(os.path.join(service_dir, "convert_out"))


The ``<token>`` has to be the same value as the JupyterHub service token specified earlier. The ``grader_service_dir`` directory has to be an existing directory with appropriate permissions to let the grader service read and write from it.

Then the grader service can be started by specifying the config file as such: ::

    grader-service -f <grader_service_config.py>

When restarting the JupyterHub you should now see the following log message: ::

    Adding external service grader at http://127.0.0.1:4010

Do not forget to set the log level to ``INFO`` in the JupyterHub config if you want to see this message.

The last thing we have to configure is the server-side of the JupyterLab plugin which also needs information where to access the endpoints of the service. This can be done in the `jupyter_notebook_config.py` file. When using the defaults from above we do not need to explicitly configure this but it would look like this: ::

    import os
    c.GitService.git_access_token = os.environ.get("JUPYTERHUB_API_TOKEN")
    c.GitService.git_remote_url = "http://127.0.0.1:4010/services/grader/git"

    c.RequestService.url = "http://127.0.0.1:4010"


