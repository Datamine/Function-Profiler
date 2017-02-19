#Function-Profiler

This is a Python 3.6 module to profile function performance. It records the number
of calls made to select functions, and outputs statistics about their execution times.

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

## Explanation, Basic Use

The profiler has three components: 

- `function_profiler`, a decorator for functions to have their calls logged
- `FunctionLogger`, a class that acts as a context manager for the decorated
    functions, and which stores (as class variables) the number of calls to each
    decorated function, as well as their execution time lengths. It also has a class
    method, `FunctionLogger.log_data`, which outputs the logged call/time data
    (to `stderr` by default).
- `with_logger`, a decorator that calls `profiler.FunctionLogger.log_data`
    after the function it wraps has exited (whether by normal return or by exception).
    This is useful if, for example, you want to output logs just once, after your
    `main` function has exited. (Or if you want to output logs every time some 
    particular function exits, etc.)

### Example     

```
import profiler

@profiler.function_profiler()
def foo():
    return

foo()
foo()
foo()

profiler.FunctionLogger.log_data('stdout')
```
output:
```
foo: 3 calls. Time stats (seconds): Min: 0.000001, Mean: 0.000002, Median: 0.000002, Max: 0.000003, Stddev: 0.000001
```

### Example

Suppose we have a file, `example.py`:

```
import profiler

@profiler.function_profiler()
def foo():
    return

@profiler.with_logger()
def main():
    foo()

if __name__=='__main__':
    main()
```
and we run this from the command line, i.e. `python3 example.py`. We get this output at the command-line:
```
foo: 1 call. Time stats (seconds): Min: 0.000001, Mean: 0.000002, Median: 0.000002, Max: 0.000003, Stddev: 0.000001
```

## Options

`profiler.FunctionLogger.log_data` takes one of three options:
- `'stdout'` if you wish the output to be logged to stdout
- `'stderr'` if you wish the output to be logged to stderr
- `'suppress'` if you wish the output not to be logged
- any other string, e.g. `'myfile.txt'` will cause the output to be logged to a file of that name.

Since `with_logger` calls `profiler.FunctionLogger.log_data`, `with_logger` also accepts
the same set of three options.

If you don't want the summary statistics but rather more granular ones, you can access
`profiler.FunctionLogger`'s class variables directly. There are two:

- `profiler.FunctionLogger.call_frequencies` is a dict mapping each function to the number of times it has been called.
- `profiler.FunctionLogger.call_times` is a dict mapping each function to a list of how long it took to complete each function call.

Finally, `profiler.function_profiler` accepts one argument: a naming convention, either 
`'qualname'` (default) or `'name'`. This is because `profiler.FunctionLogger` stores 
data on functions by using their names as keys. By default,
it uses the functions' fully qualified names in order to prevent name collisions, but by
supplying `'name'` instead, it'll just use the function's local name.

## Tests and Examples

It is possible to run tests for `profiler` before installing the module.

From the top-level directory, simply run `python3 run-tests.py`. (In order to run
the tests without installing the package, the tests use `os.getcwd()` and
then try to locate the `profiler` module using its relative path, which assumes that
the tests are being run from the top-level directory.)

Examples are located in the `examples/` directory, and should similarly be run from
the top-level directory, e.g. `python3 examples/basic-profiler.py`. If you're uncertain
about using this library, then hopefully the examples will be useful references.

## Common Errors

Note that `profiler.FunctionLogger` acts as a context manager on a function call. Consequently,
a function that does not exit will not have its call time logged. Common cases in which you
might face this error include interrupting the program before a function call finishes, or
writing a function that exceeds the maximum recursion depth (so functions are repeatedly entered, but never exited before erring).

## Compatibility

This package is intended for Python 3. It doesn't currently work for Python 2, though
it should be easy to achieve that compatibility if you need it. I am firmly moving on
to Python 3.6+, consequently I will not be writing any code to ensure backwards compatibility.
However, I am willing to bless Python 2.7-compatible forks, should they appear.

## Elsewhere

This package lives [here](https://pypi.python.org/pypi/function-profiler) on PyPI.

There's also an entry about this project [on my blog](http://www.johnloeber.com/docs/function-profiler.html").
