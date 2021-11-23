# Grader Extensions

  This repository contains the lab/server extensions and the grader service.

# Installation

## Requirements

> conda

## Creation of conda environment

Navigate to the `grader`-directory and create the environment:

    conda env create -f environment.yml

## Install convert and lab package

Start this command in both `convert`- and `grading_labextension`-directories to install them as packages

    pip install -e .
## Testing
In the root folder of the repository run

`py.test . --cov-report xml:cov.xml --cov .`

to run all tests and to generate a code coverage xml-file `cov.xml`
