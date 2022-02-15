from pathlib import Path

from setuptools import find_packages
from setuptools import setup
import os
from grader_convert.main import main

_version = "0.1.0"

source_root = Path(".")
# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

setup(
    name="grader-convert",
    version=_version, 
    packages=find_packages(".", exclude=["grader_convert.tests", "grader_convert.tests.*"]),
    package_data={"": ["templates/*.tpl"]},
    include_package_data=True,
    url="https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git",
    license="MIT",
    author='Elias Wimmer, Florian Jäger & Matthias Matt',
    author_email="",
    description="Grader convert",
    entry_points={
        "console_scripts": [
            f"grader-convert = {main.__module__}:main",
        ],
    },
    install_requires=requirements,
)