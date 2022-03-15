c.JupyterHub.services.append(
    {
        'name': 'grader',
        'url': 'http://172.19.0.3:4010',
        'api_token': 'myapitoken'
    }
)

c.JupyterHub.load_groups = {
    "lect1__instructor": ["jovyan"],
    "lect1__tutor": ["user2"],
    "lect1__student": ["user3", "user4"]
}

