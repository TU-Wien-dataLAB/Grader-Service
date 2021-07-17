from setuptools import find_packages
from setuptools import setup

_version = '0.1.0'

setup(
name='grader-service',
version=_version,
packages=find_packages(),
url='https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git',
license='MIT',
author='Elias Wimmer',
author_email='',
description='Grader service',
entry_points={
  'console_scripts': [
    'grader-service = main:main',
  ],
},
)