c.JupyterHub.services.append(
    {
        'name': 'grader',
        'url': 'http://grader_service:4010',
        'api_token': '7e272a9df62444de9d2d111b5ff6e70f'
    }
)

# c.JupyterHub.load_groups = {
#     "lect1__instructor": ["jovyan"],
#     "lect1__tutor": ["user2"],
#     "lect1__student": ["user3", "user4"]
# }

