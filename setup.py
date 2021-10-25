#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import setuptools

__version__ = "0.0.2"
__author__ = "Dave Vandenbout"
__email__ = "devb@xess.com"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md") as history_file:
    history = history_file.read().replace(".. :changelog:", "")

requirements = [
    "skidl>=1.1.0",
    "numpy",
    "sympy",
    "pint",
    "eseries",
    "importlib-metadata",
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name="circuitsascode",
    version=__version__,
    description="A collection of SKiDL modules for common electronic circuits.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url="https://github.com/devbisme/circuitsascode",
    project_urls={
        "Twitter": "https://twitter.com/circuitsascode",
        "Tracker": "https://github.com/devbisme/circuitsascode/issues",
        "Changelog": "https://github.com/devbisme/circuitsascode/latest/CHANGELOG.html",
        "Source": "https://github.com/devbisme/circuitsascode",
        "Documentation": "https://devbisme.github.io/circuitsascode",
    },
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={},
    include_package_data=False,
    scripts=[],
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="skidl kicad electronic circuit schematics",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
