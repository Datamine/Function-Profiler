# this example has to be run from the parent directory of the example
# so that the profiler can be imported from its directory
import os, sys
sys.path.append(os.getcwd())

import profiler
import time
import random

# this example essentially showcases the basic uses of
# - profiler.function_profiler
# - profiler.FunctionLogger.log_data

@profiler.function_profiler()
def foo():
    return

foo()
foo()

@profiler.function_profiler()
def bar():
    time.sleep(1)
    return

bar()

class Woz(object):

    @profiler.function_profiler()
    def __init__(self):
        self.x = 5

    @profiler.function_profiler()
    def some_instance_method(self):
        return

    @profiler.function_profiler()
    def a_class_method():
        time.sleep(random.random())
        return

woz_instance = Woz()
woz_instance.some_instance_method()

another_woz_instance = Woz()

[Woz.a_class_method() for _ in range(10)]

profiler.FunctionLogger.log_data('stdout')
