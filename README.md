#Function-Profiler

Python Module to Profile Function Performance: records the number of calls and
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
More granular reports can be accessed by calling the class variables directly.

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

## Setup Instructions

There are two ways to install this package from the terminal:

**Directly from PyPI (recommended):**

`pip install function-profiler` 

**From source:**

1. `git clone https://github.com/Datamine/Function-Profiler`
2. `cd Function-Profiler`
3. `sudo python setup.py install`

In either of these ways, you may need to swap `pip` for `pip3` or `python` 
for `python3`, depending on your local configurations.


## PyPI

This package lives [here](https://pypi.python.org/pypi?name=function-profiler&version=0.1&:action=display) on PyPI.

