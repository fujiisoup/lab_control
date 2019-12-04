#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from setuptools import setup
import re
import os
import sys

# load version form _version.py
VERSIONFILE = "lab_control/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# module

setup(name='lab_control',
      version=verstr,
      author="Keisuke Fujii",
      author_email="fujii@me.kyoto-u.ac.jp",
      description=("Python libraries for lab experiment."),
      license="BSD 3-clause",
      url="http://github.com/fujiisoup/lab_control",
      include_package_data=True,
      ext_modules=[],
      packages=["lab_control"],
      package_dir={'lab_control': 'lab_control'},
      py_modules=['lab_control.__init__'],
      install_requires="""""",
      classifiers=['License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Scientific/Engineering :: Physics']
      )
