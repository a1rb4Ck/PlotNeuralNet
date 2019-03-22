#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yapf.yapflib.yapf_api import FormatCode as _YAPF_Format

__all__ = ['FormatCode']


def FormatCode(code, filename, style_config):

    # https://pypi.python.org/pypi/yapf/0.20.2#example-as-a-module
    _, changed = _YAPF_Format(code, filename=filename, style_config=style_config, print_diff=False)

    return changed
