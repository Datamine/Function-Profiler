from time import time

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
        self.function_name = function.__name___

    def __enter__(self):
        call_frequencies[self.function_name] = call_frequencies.get(self.function_name, 0) + 1
        self.start_time = time()

    def __exit__(self):
        seconds_taken = time() - self.start_time
        call_times_so_far = call_times.get(self.function_name, [])
        call_times[self.function_name] = call_times + [seconds_taken]

    def log_data(self):
        print(call_frequencies)
        print(call_times)


def counted(function):
    """
    counts the number of times a function was called.
    """
    def wrapper(*args, **kwargs):
        with FunctionLogger(function):
            return function(*args, **kwargs)
    return wrapper

