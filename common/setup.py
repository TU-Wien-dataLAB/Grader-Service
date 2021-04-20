from setuptools import find_namespace_packages
from setuptools import setup

setup(
name='grader.common',
version='0.1.0',
packages=find_namespace_packages(include=['grader.*']),
# package_dir={'': 'grader/common'},
url='https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git',
license='MIT',
author='Florian Jäger',
author_email='',
description='Common library of grader'
)