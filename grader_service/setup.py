from setuptools import find_packages
from setuptools import setup
import os
from grader_service.main import main

_version = '0.1.0'

setup(
    name='grader-service',
    version=_version,
    packages=find_packages(".", exclude=["grader_service.tests", "grader_service.tests.*"]),
    package_data={'grader_service': ['./grader_service/alembic.ini']},
    include_package_data=True,
    url='https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git',
    license='MIT',
    author='Florian Jäger & Matthias Matt',
    author_email='',
    description='Grader service',
    entry_points={
        'console_scripts': [
            f'grader-service = {main.__module__}:main',
        ],
    },
)
