from setuptools import find_packages
from setuptools import setup
import os
from grader_convert.main import main

_version = "0.1.0"
HERE = os.path.dirname(__file__)
package_dir = os.path.join(HERE, "grader_convert")

setup(
    name="grader-convert",
    version=_version, 
    packages=find_packages(".", exclude=["grader_convert.tests", "grader_convert.tests.*"]),
    package_data={"": ["templates/*.tpl"]},
    include_package_data=True,
    url="https://gitlab.tuwien.ac.at/hpc/datalab/jupyter/grader/grader.git",
    license="MIT",
    author="Matthias Matt",
    author_email="",
    description="Grader convert",
    entry_points={
        "console_scripts": [
            f"grader-convert = {main.__module__}:main",
        ],
    },
)