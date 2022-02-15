from pathlib import Path

from setuptools import find_packages
from setuptools import setup
import os
from grader_service.main import main
from grader_service.alembic.migrate import main as migrate_main

_version = '0.1.0'

source_root = Path(".")
# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

setup(
    name='grader-service',
    version=_version,
    packages=find_packages(".", exclude=["grader_service.tests", "grader_service.tests.*"]),
    package_data={'grader_service.alembic': ['alembic.ini']},
    url='https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git',
    license='MIT',
    author='Elias Wimmer, Florian Jäger & Matthias Matt',
    author_email='',
    description='Grader service',
    entry_points={
        'console_scripts': [
            f'grader-service = {main.__module__}:main',
            f'grader-service-migrate = {migrate_main.__module__}:main'
        ],
    },
    python_requires=">=3.8",
    install_requires=requirements,
)
