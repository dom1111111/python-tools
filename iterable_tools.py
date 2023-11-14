"""
Functions to use with iterables
"""

def flatten_generator(iterable:list|tuple):
    """Pass in a list or tuple which can have any number of lists/tuples 
    or non iterable items within, as well as any abitrary depth for further 
    nested lists/tuples, and get back a flattened iterable generator."""
    for item in iterable:
        if isinstance(item, list) or isinstance(item, tuple):
            yield from flatten_generator(item)                  # very handy! - https://docs.python.org/3/whatsnew/3.3.html#pep-380-syntax-for-delegating-to-a-subgenerator
        else:
            yield item