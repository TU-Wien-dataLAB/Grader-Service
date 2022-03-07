# Grader Extensions

  This repository contains the lab/server extensions, grader-convert package and the grader service.

## Requirements

> JupyterHub, Python 3.8,
> pip,
> npm

# Manual Installation

## 1. Grader Convert Installation
Navigate to the `convert` directory and install the package requirements with the package manager `pip`

    pip install -r requirements.txt

Install the convert package

    pip install -e .

## 2. Grader Service Installation

Navigate to the `grader_service`-directory and install the package requirements:

    pip install -r requirements.txt

Install the grader service package

    pip install -e .

## 3. Jupyter Extensions Installation

Navigate to the `grading_labextension`-directory and follow the instructions in the README file

## Testing
In the root folder of the repository run

`py.test . --cov-report xml:cov.xml --cov .`

to run all tests and to generate a code coverage xml-file `cov.xml`
