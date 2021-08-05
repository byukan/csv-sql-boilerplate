#!/usr/bin/env python3
"""
:file: test_most_active_cookie.py
:author: Brant Yukan
:date: 8/4/21
:brief: This program runs unit tests and logs output in tests.log.
"""
import sys
import unittest
from importlib.machinery import SourceFileLoader


class MyTestCase(unittest.TestCase):
    def test_query(self):
        """
        Tests for correct query output for various dates and multiple cookies on given sample cookie log data.
        """
        module = SourceFileLoader('__main__', 'most_active_cookie.py').load_module()
        sys.argv = './most_active_cookie cookie_log.csv -d 2018-12-08'.split(' ')
        self.assertEqual(module.main(), {'SAZuXPGUrfbcn5UA', '4sMM2LxV07bPJzwf', 'fbcn5UAVanZf6UtG'})

        sys.argv = './most_active_cookie cookie_log.csv -d 2018-12-09'.split(' ')
        self.assertEqual(module.main(), {'AtY0laUfhglK3lC7'})


if __name__ == '__main__':
    unittest.main()
