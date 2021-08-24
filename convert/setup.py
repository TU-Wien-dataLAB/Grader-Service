from setuptools import find_packages
from setuptools import setup

_version = '0.1.0'

setup(
name='grader-convert',
version=_version,
packages=find_packages(exclude=("tests",)),
url='https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git',
license='MIT',
author='Matthias Matt',
author_email='',
description='Grader convert',
entry_points={
  'console_scripts': [
    'grader-convert = main:main',
  ],
},
)