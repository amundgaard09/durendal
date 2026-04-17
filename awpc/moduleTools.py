"""Module for various data extraction tasks on modules in Python. Built on top of the `inspect` library"""

import inspect

from awpc.unimath import unimath
from awpc.unicrypt import unicrypt

def genDict(Module) -> tuple[dict, dict]:
    """Generate an argument count dict and function call dict for a module. Returns `(arg_count_dict, call_dict)`, both in alphabetical order."""
    
    arg_count_dict = {}
    call_dict = {}
    
    for name, obj in inspect.getmembers(Module, inspect.isfunction):
    
        if name.startswith("_"):
            continue

        sig = inspect.signature(obj)

        param_count = sum(
            1 for p in sig.parameters.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
        )

        if name not in arg_count_dict:
            arg_count_dict[name] = set()
        arg_count_dict[name].add(param_count)

        call_dict[name] = obj
    
    return arg_count_dict, call_dict

UNIMATHARGMAP, UNIMATHCALLMAP = genDict(unimath)
UNICRYPTARGMAP, UNICRYPTCALLMAP = genDict(unicrypt)