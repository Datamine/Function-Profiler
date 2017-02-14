from time import time
from sys import stderr, stdout
import numpy as np

"""
Implements a decorator that counts the number of times a function was called,
and collects stats on how long it took to execute every single function call.
"""

class FunctionLogger(object):
    """
    stores two dictionaries:
        - call_frequencies: mapping of function names to counts of how often they've been called
        - call_times: mapping of functon names to lists of how long it took to execute a fn call
    """
    call_frequencies = {}
    call_times = {}

    def __init__(self, function):
        self.function_name = function.__name__

    def __enter__(self):
        FunctionLogger.call_frequencies[self.function_name] = FunctionLogger.call_frequencies.get(self.function_name, 0) + 1
        self.start_time = time()

    def __exit__(self, type, value, traceback):
        seconds_taken = time() - self.start_time
        call_times_so_far = FunctionLogger.call_times.get(self.function_name, [])
        FunctionLogger.call_times[self.function_name] = call_times_so_far + [seconds_taken]

    def log_data(output_option):
        """
        logs the class variables to stdout, stderr, or to a file.
        """
        for function_key in FunctionLogger.call_frequencies.keys():
            call_freq = FunctionLogger.call_frequencies.get(function_key, 0)
            call_times = FunctionLogger.call_times.get(function_key, [])

            stats_string = "No stats were recorded for this function. This is most likely an error."
            if call_times != []:
                # call_times == [] iff __enter__ was called with some function, but __exit__ was not
                stats_string = "Min: {:08f}, Mean: {:08f}, Median: {:08f}, Max: {:08f}".format(np.min(call_times), np.mean(call_times), np.median(call_times), np.max(call_times))

            if call_freq != len(call_times):
                # then the __exit__ was not called due to some error. attach a warning.
                stats_string += ("\nWARNING: number of call times ({}) is not equal to call frequency count ({}). "
                                "Suggests the program terminated while the function was running.\n").format(len(call_times), call_freq)

            out_string = ("{}: {} calls. Time stats (seconds): " + stats_string + "\n").format(function_key, call_freq)

            if output_option == 'stdout':
                stdout.write(out_string)
            elif output_option == 'stderr':
                stderr.write(out_string)
            else:
                with open(output_option, "w") as log_file:
                    log_file.write(out_string)


def function_profiler(function):
    """
    decorator that uses FunctionLogger to log information about this call of the function.
    """
    def wrapper(*args, **kwargs):
        with FunctionLogger(function):
            return function(*args, **kwargs)
    return wrapper

