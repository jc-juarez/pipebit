# -------------------------------
# PipeBit
# 'setup.py'
# Author: Juan Carlos Juárez.
# Licensed under MPL 2.0.
# All rights reserved.
# -------------------------------

from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'PipeBit'
LONG_DESCRIPTION = 'PipeBit is a Quick Pipeline Management System for Local Data Pipelines.'

# Setting up
setup(
    name="pipebit",
    version=VERSION,
    author="Juan Carlos Juárez",
    author_email="<jc.juarezgarcia@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['Pipelines', 'Python', 'Tool'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)