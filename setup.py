#!/usr/bin/python
#
# Copyright 2008 Alberto Milone <albertomilone@alice.it>

from distutils.core import setup

import subprocess, glob, os.path

setup(
    name="xkit",
    author="Alberto Milone",
    author_email="albertomilone@alice.it",
    maintainer="Alberto Milone",
    maintainer_email="albertomilone@alice.it",
    url="https://launchpad.net/x-kit",
    license="GPL v2 or later",
    description="library for the manipulation of the xorg.conf",
    packages=["XKit"],
    scripts=[],
)





