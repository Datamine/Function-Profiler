#!/usr/bin/python3
"""
tests for profiler/profiler.py
"""

import unittest
from unittest import mock
import os, sys
sys.path.append(os.getcwd())

import profiler

class FunctionLogger(unittest.TestCase):
    """
    tests specifically for the modular functions in profiler.FunctionLogger
    TODO: log_data function remains untested. Tests for the output are both
    somewhat tedious to implement, as well as trivial. The important logic
    is in make_output_string, and is tested appropriately.
    """

    def setUp(self):
        """
        Because profiler.FunctionLogger relies on mutable class variables, we need
        to reset them between every set of tests.
        """
        profiler.FunctionLogger.clear_data()

    def test_clear_data(self):
        """
        Tests that profiler.FunctionLogger.clear_data() clears the class variables
        as expected.
        """

        @profiler.function_profiler()
        def foo():
            return
        foo()
        foo()

        self.assertNotEqual(profiler.FunctionLogger.call_frequencies, {})
        self.assertNotEqual(profiler.FunctionLogger.call_times, {})

        profiler.FunctionLogger.clear_data()

        self.assertEqual(profiler.FunctionLogger.call_frequencies, {})
        self.assertEqual(profiler.FunctionLogger.call_times, {})

class WithLogger(unittest.TestCase):
    """
    This suite tests that the decorator profiler.with_logger wraps a function
    and calls FunctionLogger.log_data after the wrapped function terminates.
    """

    def setUp(self):
        """
        Because profiler.FunctionLogger relies on mutable class variables, we need
        to reset them between every set of tests.
        """
        profiler.FunctionLogger.clear_data()
        self.mock_log_data = mock.Mock(wraps=profiler.FunctionLogger.log_data)

    def test_normal_termination(self):
        """
        tests that log_data is called when the function wrapped by
        profiler.with_logger terminates as usual
        """

        @profiler.function_profiler()
        def foo():
            return

        @profiler.with_logger()
        def bar():
            foo()

        with mock.patch.object(profiler.FunctionLogger, 'log_data') as monkey:
            bar()

        monkey.assert_called_once()

    def test_error_termination(self):
        """
        tests that log_data is called when the function wrapped by
        profiler.with_logger terminates due to an Exception
        """

        @profiler.function_profiler()
        def foo():
            return

        @profiler.with_logger()
        def bar():
            foo()
            raise Exception("This function hits an error!")

        try:
            with mock.patch.object(profiler.FunctionLogger, 'log_data') as monkey:
                bar()
        except:
            pass

        monkey.assert_called_once()

class General(unittest.TestCase):
    """
    This suite tests general of both the decorator profiler.function_profiler
    and the class profiler.FunctionLogger.
    """

    def setUp(self):
        """
        Because profiler.FunctionLogger relies on mutable class variables, we need
        to reset them between every set of tests.
        """
        profiler.FunctionLogger.clear_data()

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
        self.assertCountEqual(profiler.FunctionLogger.call_times.keys(), [foo_name])

    def test_decorator_bad_naming(self):
        """
        Tests that naming arguments other than 'qualname' or 'name', if supplied to the decorator,
        cause an error to be thrown.
        """
        bad_name = "blah"
        exception_msg = "Invalid naming argument supplied to function_profiler: " + bad_name
        with self.assertRaises(ValueError, msg=exception_msg):
            @profiler.function_profiler(bad_name)
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

        profiler.FunctionLogger.log_data('suppress')

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
        self.assertCountEqual(
            profiler.FunctionLogger.call_times.keys(),
            ["__init__", additional_function_qualname]
        )

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

class MakeOutputString(unittest.TestCase):
    """
    Tests for the function profiler.make_output_string
    """

    def test_with_empty_call_times(self):
        log = profiler.make_output_string('foo', [], 5)
        expected_log = (
            "foo: 5 calls. Time stats (s): No time stats were recorded for this "
            "function, despite it having been called. This is an error.\n"
            "WARNING: number of call times (0) is not equal to call frequency count "
            "(5). This suggests the function was called, but did not return as normal. "
            "Check for errors or program termination.\n"
        )

        self.assertEqual(log, expected_log)

    def test_with_unequal_call_times_and_freqs(self):
        log = profiler.make_output_string('foo', [3, 4, 5], 10)
        expected_log = (
            "foo: 10 calls. Time stats (s): Min: 3.000000, Max: 5.000000, Mean: 4.000000, "
            "Median: 4.000000, Stddev: 0.816497\n"
            "WARNING: number of call times (3) is not equal to call frequency count (10). "
            "This suggests the function was called, but did not return as normal. Check "
            "for errors or program termination.\n"
        )

        self.assertEqual(log, expected_log)

    def test_with_equal_call_times_and_freqs(self):
        log = profiler.make_output_string('foo', [3, 4, 5], 3)
        expected_log = (
            "foo: 3 calls. Time stats (s): Min: 3.000000, Max: 5.000000, Mean: 4.000000, "
            "Median: 4.000000, Stddev: 0.816497\n"
        )

        self.assertEqual(log, expected_log)

    def test_with_one_call(self):
        log = profiler.make_output_string('foo', [3], 1)
        expected_log = (
            "foo: 1 call. Time stats (s): Min: 3.000000, Max: 3.000000, Mean: 3.000000, "
            "Median: 3.000000, Stddev: 0.000000\n"
        )

        self.assertEqual(log, expected_log)

if __name__=='__main__':
    unittest.main()
