# Grader Extensions

  This repository contains the lab/server extensions and the grader service.

# Installation

This repository contains all the necessary packages for a full installation of the grader service.

- `grader-convert`: A tool for converting notebooks to different formats (e.g. removing solution code, executing, etc.). It can be used as a command line tool but will mainly be called by the service.
- `grading_labextension`: The JupyterLab plugin for interacting with the service. Provides the UI for instructors and students and manages the local git repositories for the assignments etc.
- `grader-service`: Manages students and instructors, files, grading and multiple lectures. It can be run as a standalone containerized service and can utilize a kubernetes cluster for grading assignments.


## Requirements

> JupyterHub, Python 3.8,
> pip,
> Node.js
> npm

# Manual Installation

## Local installation
Navigate to the `convert` directory and install the package requirements with the package manager `pip`

In the `grader` directory run:

    pip install ./convert
    pip install ./grading_labextension
    pip install ./grader_service

Then, navigate to the `grading_labextension`-directory and follow the instructions in the README file

## Running grader service
To run the grader service you first have to register the service in JupyterHub as an unmanaged service in the config:

    c.JupyterHub.services.append(
        {
            'name': 'grader',
            'url': 'http://127.0.0.1:4010',
            'api_token': '<token>'
        }
    )
