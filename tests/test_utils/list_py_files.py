#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
from tests.test_utils import DIRS_TO_CHECK_4_STYLE

__all__ = [
    'list_all_py_files',
]

_excludes = []


def list_all_py_files():

    # Project Root Dir - Not Recursive
    for file in glob.iglob("*.py"):
        yield file

    for dir in DIRS_TO_CHECK_4_STYLE:

        if dir in _excludes:
            continue

        for file in glob.iglob("%s/**/*.py" % dir, recursive=True):
            yield file
