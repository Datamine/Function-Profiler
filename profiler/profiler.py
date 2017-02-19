"""
Implements a decorator that counts the number of times a function was called,
and collects statistics on how long it took to execute every single function call.
"""

from time import time
from sys import stderr, stdout
import numpy as np

class FunctionLogger(object):
    """
    stores two dictionaries:
        - call_frequencies: mapping of function names to counts of how often they've been called
        - call_times: mapping of function names to lists of how long it took to execute a fn call
    """
    call_frequencies = {}
    call_times = {}

    def __init__(self, function, naming):
        """
        initialize an instance of FunctionLogger. Notably, the user should not ever have
        to do this: this exists solely to create a context manager for function_profiler.
        """
        self.start_time = None

        if naming == 'qualname':
            self.function_name = function.__qualname__
        elif naming == 'name':
            self.function_name = function.__name__
        else:
            raise ValueError(
                "Invalid naming argument supplied to function_profiler: %s"
                .format(naming)
            )

    def __enter__(self):
        FunctionLogger.call_frequencies[self.function_name] = (
            FunctionLogger.call_frequencies.get(self.function_name, 0) + 1
        )
        self.start_time = time()

    def __exit__(self, type_, value, traceback):
        seconds_taken = time() - self.start_time
        call_times_so_far = FunctionLogger.call_times.get(self.function_name, [])
        FunctionLogger.call_times[self.function_name] = call_times_so_far + [seconds_taken]

    def clear_data():
        """
        Clears the data stored in the class variables. No 'self' argument
        because this is not run on an instance, but on the class itself.
        """
        FunctionLogger.call_frequencies = {}
        FunctionLogger.call_times = {}

    def log_data(output_option='stderr'):
        """
        logs the class variables to stdout, stderr, or to a file. No 'self' arg
        because this is not run on an instance, but on the class itself.
        """

        # for when we're logging to a file, rather than stderr or stdout
        log_file_strings = []

        for function_key in sorted(FunctionLogger.call_frequencies.keys()):
            call_freq = FunctionLogger.call_frequencies.get(function_key, 0)
            call_times = FunctionLogger.call_times.get(function_key, [])
            out_string = make_output_string(function_key, call_times, call_freq)

            if output_option == 'stderr':
                stderr.write(out_string)
            elif output_option == 'stdout':
                stdout.write(out_string)
            else:
                log_file_strings.append(out_string)

        if log_file_strings:
            with open(output_option, 'w') as out_file:
                for out_string in log_file_strings:
                    out_file.write(out_string)

def make_output_string(fn_name, call_times, call_freq):
    """
    Construct a string that represents the log for this one particular function.
        - fn_name: string, name of the function
        - call_times: list of floats (lengths of function calls)
        - call_freq: integer, number of times the function was called
    """

    if call_times == []:
        # call_times == [] iff __enter__ was called with this fn, but __exit__ was not
        stats_string = (
            "No time stats were recorded for this function, "
            "despite it having been called. This is an error.\n"
        )
    else:
        stats_string = (
            "Min: {:08f}, Max: {:08f}, Mean: {:08f}, Median: {:08f}, Stddev: {:08f}\n"
            .format(np.min(call_times), np.max(call_times), np.mean(call_times),
                    np.median(call_times), np.std(call_times))
        )

    if call_freq != len(call_times):
        # for at least one call of this function, __enter__ was called but __exit__ was not.
        stats_string += (
            ("WARNING: number of call times ({}) is not equal to call frequency count ({}). "
             "This suggests the function was called, but did not return as normal. Check "
             "for errors or program termination.\n").format(len(call_times), call_freq)
        )

    call_text = "call" if (call_freq == 1) else "calls"

    return "{}: {} {}. Time stats (s): {}".format(fn_name, call_freq, call_text, stats_string)

def function_profiler(naming='qualname'):
    """
    decorator that uses FunctionLogger as a context manager to
    log information about this call of the function.
    """
    def layer(function):
        def wrapper(*args, **kwargs):
            with FunctionLogger(function, naming):
                return function(*args, **kwargs)
        return wrapper
    return layer

def with_logger(output='stderr'):
    """
    decorator that calls FunctionLogger.log_data when the decorated function
    terminates, whether due to an exception or not.
    """
    def layer(function):
        def wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
            finally:
                FunctionLogger.log_data(output)
        return wrapper
    return layer
