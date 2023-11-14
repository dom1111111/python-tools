"""
Functions for easier to read printing in the terminal
"""

from string_tools import get_clean_keyvalue_spacing, box_text

def nl_print(*message):
    """Same as default `print()` function but with an extra line break!"""
    print()
    print(*message)

def print_dict_nicely(d:dict, max_spacing:int=5):
    """print all keys and values in a dictionary with consistent spacing inbetween them"""
    max_spacing = 5 + len(str(max(d.keys(), key=len)))
    for k, v in d.items():
        print(get_clean_keyvalue_spacing(k, v, max_spacing))
