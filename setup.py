# -*- coding: utf-8 -*-
"""
Setup.py file
"""

import re
import sys
import io
import os
from setuptools import setup, find_packages, Command

AUTHOR = "Tree"
EMAIL = "2332532718@qq.com"
URL = ""

NAME = "Cartoon Extractor"
DESCRIPTION = """
A Tool for Cartoon Extractor
"""
REQUIRES_PYTHON = ">2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*"
REQUIRED = [
    "requests", "beautifulsoup4",
]

here = os.path.dirname(__name__)
readme = io.open(os.path.join(here, "README.md"), encoding="utf-8").read()

about = io.open(os.path.join(here, 'src', 'cartoon', '__init__.py'), encoding='utf-8').read()
VERSION = re.findall(r'^__version__ *= *(.+?) *$', about, re.M)[0][1:-1]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,

    packages=find_packages("src"),
    package_dir={"": "src"},

    include_package_data=True,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='MIT',
    entry_points={'console_scripts': ['ct-get = cartoon.cli:main']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
)
