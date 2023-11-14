"""
Just a reference for JSON `load` and `dump` functions 
"""

import json

storage_path = ""
a_list = []

# load
with open(storage_path, 'r') as f:
    a_list.extend(json.load(f))

# dump
with open(storage_path, 'w') as f:
    json.dump(a_list, f, indent=1)
