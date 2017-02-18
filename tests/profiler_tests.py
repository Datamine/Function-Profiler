#!/usr/bin/python3
"""
tests for profiler/profiler.py
"""

import unittest
import os, sys
sys.path.append(os.getcwd())

import profiler

class FunctionLogger(unittest.TestCase):
    """

    """
    pass

class FunctionProfiler(unittest.TestCase):
    """
    tests for profiler.function_profiler
    """
    pass

class General(unittest.TestCase):
    """
    This suite tests general use of the decorator, i.e. both the decorating function
    profiler.function_profiler and the class profiler.FunctionLogger.
    """

    def setUp(self):
        """
        Because profiler.FunctionLogger relies on mutable class variables, we need
        to reset them between every set of tests.
        """
        profiler.FunctionLogger.call_frequencies = {}
        profiler.FunctionLogger.call_times = {}

    def test_decorator_default_naming(self):
        """
        Testing that the decorator defaults to 'qualname', and that the keys in
        profiler.FunctionLogger.call_frequencies, call_times are written appropriately
        """

        @profiler.function_profiler()
        def foo():
            return
        foo()

        # not obtainable via foo.__qualname__ because of the doubly-wrapping decorator
        foo_qualname = "General.test_decorator_default_naming.<locals>.foo"
        self.assertEqual(profiler.FunctionLogger.call_frequencies, {foo_qualname: 1})
        self.assertEqual(list(profiler.FunctionLogger.call_times.keys()), [foo_qualname])

    def test_decorator_optional_naming(self):
        """
        Testing that when 'name' is supplied to the decorator, then the keys in
        profiler.FunctionLogger.call_times, call_frequencies are names, not necessarily qualnames
        """

        @profiler.function_profiler('name')
        def foo():
            return
        foo()

        foo_name = "foo"
        self.assertEqual(profiler.FunctionLogger.call_frequencies, {foo_name: 1})
        self.assertEqual(list(profiler.FunctionLogger.call_times.keys()), [foo_name])

    def test_decorator_bad_naming(self):
        """
        Tests that naming arguments other than 'qualname' or 'name', if supplied to the decorator,
        cause an error to be thrown.
        """
        with self.assertRaises(ValueError):
            @profiler.function_profiler("blah")
            def foo():
                return
            foo()

    def test_multiple_uses(self):
        """
        test that even when using the decorator on several functions,
        the instance variables of FunctionLogger do not conflict; and all
        information is stored in the class variables as expected.
        """

        # We'll use the 'name' flag fo easy testing because qualnames
        # produce unweildy results in these unittests
        @profiler.function_profiler('name')
        def foo():
            return
        foo()

        @profiler.function_profiler('name')
        def bar():
            return 1
        foo()
        bar()
        foo()
        bar()
        bar()

        @profiler.function_profiler('name')
        def baz():
            return 2
        baz()
        foo()

        profiler.FunctionLogger.log_data('output')

        expected_call_frequencies = {"foo": 4, "bar": 3, "baz": 1}
        self.assertCountEqual(profiler.FunctionLogger.call_frequencies, expected_call_frequencies)
        self.assertCountEqual(profiler.FunctionLogger.call_times.keys(), ["foo", "bar", "baz"])
        self.assertEqual(len(profiler.FunctionLogger.call_times["foo"]), 4)
        self.assertEqual(len(profiler.FunctionLogger.call_times["bar"]), 3)
        self.assertEqual(len(profiler.FunctionLogger.call_times["baz"]), 1)

    def test_on_class_methods(self):
        """
        test that the decorator behaves as expected on a class method.
        """

        class Foo(object):
            # One example with 'name', one with 'qualname' to underscore that
            # qualnames work as expected
            @profiler.function_profiler('name')
            def __init__(self, x):
                self.x = x

            @profiler.function_profiler()
            def additional_function(self):
                return 5

        instance_one = Foo(5)
        instance_two = Foo(6)
        instance_two.additional_function()
        instance_three = Foo(8)
        instance_three.additional_function()

        additional_function_qualname = "General.test_on_class_methods.<locals>.Foo.additional_function"
        expected_call_frequencies = {"__init__": 3, additional_function_qualname: 2}
        self.assertCountEqual(profiler.FunctionLogger.call_frequencies, expected_call_frequencies)
        self.assertCountEqual(profiler.FunctionLogger.call_times.keys(), ["__init__", additional_function_qualname])

    def test_args_and_kwargs(self):
        """
        Make sure that the function call is not impeded by the decorator,
        i.e. that the decorated function still outputs as expected.
        """

        @profiler.function_profiler('name')
        def foo(a, b, c, d):
            return a * b * c * d
        foo_call = foo(2, 3, c=7, d=11)

        self.assertEqual(foo_call, 462)
        self.assertCountEqual(profiler.FunctionLogger.call_frequencies, {"foo": 1})

if __name__=='__main__':
    unittest.main()
