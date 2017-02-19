# this example has to be run from the parent directory of the example
# so that the profiler can be imported from its directory
import os, sys
sys.path.append(os.getcwd())

import profiler

# this example shows how to use profiler.with_logger to log the data
# on program termination. Note that the with_logger decorator will log
# even in the event of its decorated function (main) raising an error.

@profiler.function_profiler()
def foo():
    return

@profiler.with_logger()
def main():
    foo()
    foo()

if __name__=='__main__':
    main()
