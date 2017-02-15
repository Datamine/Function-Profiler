#!/usr/bin/python3
"""
tests for profiler/profiler.py
"""

import unittest
import os, sys
sys.path.append(os.getcwd())

from profiler import profiler

class FunctionLogger(unittest.TestCase):
    pass

class FunctionProfiler(unittest.TestCase):
    pass

class General(unittest.TestCase):

    def test_general_use(self):

        import profiler
        @profiler.function_profiler
        def foo():
            return
        foo()
        foo()
        foo()
        profiler.FunctionLogger.log_data()

if __name__=='__main__':
    unittest.main()
