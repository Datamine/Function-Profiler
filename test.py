#!/usr/bin/python3

import profiler

@profiler.function_profiler
def foo():
    return

foo()
foo()
foo()

profiler.FunctionLogger.log_data('stdout')
