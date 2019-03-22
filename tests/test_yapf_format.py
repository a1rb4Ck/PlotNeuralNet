#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

parent_dir = os.path.sep.join(sys.path[0].split(os.path.sep)[:-1])
sys.path.append(parent_dir)

from tests.test_utils import list_all_py_files
from tests.test_utils import CustomTestCase
from tests.test_utils.yapf_api import FormatCode

YAPF_STYLE_FILE = '.style.yapf'


def _read_utf_8_file(filename):
    if sys.version_info.major == 2:  ## Python 2 specific
        with open(filename, 'rb') as f:
            return unicode(f.read(), 'utf-8')
    else:
        with open(filename, encoding='utf-8') as f:
            return f.read()


class YAPF_Style_Test(CustomTestCase):

    @classmethod
    def setUpClass(cls):

        cls.badly_formatted_files = list()
        cls.files_2_test = list_all_py_files()

    def test_files_format(self):

        for file in list_all_py_files():

            try:

                print(file)
                code = _read_utf_8_file(file)

                # https://pypi.python.org/pypi/yapf/0.20.2#example-as-a-module
                need_changes = FormatCode(code, filename=file, style_config=YAPF_STYLE_FILE)

                if need_changes:
                    self.badly_formatted_files.append(file)

            except Exception as e:
                print("Error while processing file: `%s`\n" "Error: %s" % (file, str(e)))

        with self.assertNotRaises(Exception):

            str_err = ""

            if self.badly_formatted_files:
                for filename in self.badly_formatted_files:
                    str_err += 'yapf -i --style=%s %s\n' % (YAPF_STYLE_FILE, filename)

                str_err = "\n======================================================================================\n" \
                          "Bad Coding Style: %d file(s) need to be formatted, run the following commands to fix: \n%s" \
                          "======================================================================================" % (
                    len(self.badly_formatted_files), str_err)

                raise Exception(str_err)


if __name__ == '__main__':
    unittest.main()
