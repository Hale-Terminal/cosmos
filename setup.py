from importlib.metadata import entry_points
import os
import sys
from setuptools import setup


def get_requirements():
    with open("requirements.txt") as f:
        return [x.strip() for x in f.read().split("\n") if not x.startswith('#')]


install_requires = get_requirements()

setup(
    name="cosmos",
    version="0.0.1",
    package_dir={"cosmos": "cosmos"},
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["cosmos = cosmos.cli:entrypoint"]
    }
)