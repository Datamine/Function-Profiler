#Function-Profiler

Python module to profile function performance: records the number of calls and
outputs statistics about function execution times.

## Compatibility

This package is intended for Python 3. It may also work for Python 2, but this 
compatibility will not be ensured or tested for.

## Explanation & Example

The profiler has two components: a decorator and a class. The decorator, `@profiler.function_profiler`,
uses the `profiler.FunctionLogger` class as a context manager. 
The `FunctionLogger` incrementally stores, as *class variables*, the number of calls 
to each decorated function, as well as how long it took to execute each function. 
A summary of this data can then be printed in the end using the `log_data` method.

```
import profiler

@profiler.function_profiler
def foo():
    return

foo()
foo()
foo()

profiler.FunctionLogger.log_data('stdout')
```
output:
```
foo: 3 calls. Time stats (seconds): Min: 0.000001, Mean: 0.000002, Median: 0.000001, Max: 0.000003
```

## Advanced Options

`profiler.FunctionLogger.log_data` takes one of three options:
- `'stdout'` if you wish the output to be logged to stdout
- `'stderr'` if you wish the output to be logged to stderr
- any other string, e.g. `'myfile.txt'` will cause the output to be logged to a file of that name.

If you don't want the summary statistics but rather more granular ones, you can access
`profiler.FunctionLogger`'s class variables directly. There are two relevant ones:

- `profiler.FunctionLogger.call_frequencies` is a dict mapping each function to the number of times it has been called.
- `profiler.FunctionLogger.call_times` is a dict mapping each function to a list of how long it took to complete each function call.

## Setup

There are two ways to install this package from the terminal:

**Directly from PyPI (recommended):**

`pip3 install function-profiler` 

**From source:**

1. `git clone https://github.com/Datamine/Function-Profiler`
2. `cd Function-Profiler`
3. `sudo python3 setup.py install`

In either of these ways, it may be acceptable to use `pip` or `python` instead of
`pip3` and `python3` respectively, depending on your local configuration.

## Tests

It is possible to run tests for `profiler` before installing the module.

From the top-level directory, simply run `python3 run-tests.py`. (In order to run
the tests without installing the package, the tests use `os.getcwd()` and
then try to locate the `profiler` module using its relative path, which assumes that
the tests are being run from the top-level directory.)

## Common Errors

Note that `profiler.FunctionLogger` acts as a context manager on a function call. Consequently,
a function that does not exit will not have its call time logged. Common cases in which you
might face this error include interrupting the program before a function call finishes, or
writing a function that exceeds the maximum recursion depth (so functions are repeatedly entered, but never exited before erring).

## PyPI

This package lives [here](https://pypi.python.org/pypi/function-profiler) on PyPI.

