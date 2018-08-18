#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
import re

from setuptools import find_packages, setup, Command

# Package meta-data
NAME='aapg'
DESCRIPTION = 'Automatic Assembly Generator for RISC-V'
AUTHOR = 'Anmol Sahoo'
EMAIL = 'shakti@iitm.ac.in'
VERSION = None

REQUIRED = [
    'six',
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding = 'utf-8') as f:
    long_description = '\n' + f.read()

if not VERSION:
    with io.open(os.path.join(here, NAME, '__version__.py')) as f:
        VERSION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': ['aapg=aapg.main:execute'],
    },
    install_requires=REQUIRED,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
