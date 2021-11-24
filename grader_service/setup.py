from setuptools import find_packages
from setuptools import setup
import os
from service.main import main

_version = '0.1.0'
HERE = os.path.dirname(__file__)
package_dir = os.path.join(HERE, "grader_convert")

setup(
    name='grader-service',
    version=_version,
    packages=find_packages(".", exclude=["service.tests", "service.tests.*"]),
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
