#!/usr/bin/python3
"""
script to run all tests in the tests/ directory.
adapted from http://stackoverflow.com/a/40437679
"""

import unittest
loader = unittest.TestLoader()
start_dir = './tests/'
suite = loader.discover(start_dir, "*")

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
