"""
Functions for testing functions
"""

from time import time

def get_func_execution_time(n:int, func, *args):
    """
    get the time (in seconds) that a function takes to execute
    - `func` - function/method to test
    - `args` - arguments to pass to the test function/method
    - `n` - number of times to execute
    """
    t1 = time()
    for x in range(n):
        func(*args)
    t2 = time()
    return t2 - t1