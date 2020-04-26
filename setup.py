# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = "watersnake"
DESCRIPTION = "Watermarking in Python"
HOMEPAGE = "https://github.com/jcklie/watersnake"
EMAIL = "git@mrklie.com"
AUTHOR = "Jan-Christoph Klie"
REQUIRES_PYTHON = ">=3.5.0"

install_requires = [
    "numpy",
    "scipy",
    "pillow"
]

test_dependencies = [
    "tox",
    "codecov",
    "imageio",
    "scikit-image"
]

dev_dependencies = [
    "black",
]

doc_dependencies = [
    "sphinx",
    "sphinx-autodoc-typehints",
    "sphinx-rtd-theme"
]

extras = {
    "test": test_dependencies,
    "dev": dev_dependencies,
    "doc": doc_dependencies
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "watersnake", "__version__.py")) as f:
    exec(f.read(), about)


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=HOMEPAGE,
    packages=find_packages(exclude="tests"),
    keywords="watermarking",

    project_urls={
        "Bug Tracker": "https://github.com/jcklie/watersnake/issues",
        "Documentation": "https://github.com/jcklie/watersnake",
        "Source Code": "https://github.com/jcklie/watersnake",
    },

    install_requires=install_requires,
    test_suite="tests",

    tests_require=test_dependencies,
    extras_require=extras,

    include_package_data=True,
    license="Apache License",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics"
    ]
)