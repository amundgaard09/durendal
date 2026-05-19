"""Module for various data extraction tasks on modules in Python. Built on top of the `inspect` library"""

import inspect

from awpc.src.unipy.uniflight import uniflight
from awpc.src.unipy.unispace import unispace
from awpc.src.unipy.unicrypt import unicrypt
from awpc.src.unipy.unipower import unipower
from awpc.src.unipy.uniphys import mechanics
from awpc.src.unipy.unimath import unimath
from awpc.src.unipy.unialgo import unialgo

def _generateDicts(Module) -> tuple[dict, dict]:
    """
    Generate an argument count dict and function call dict for a module. 
    
    Returns 
    -------
    - `arg_dict`:  A dict with the function(s) as a key and the number of valid arguments as a set.
    - `call_dict`: A dict with the function(s) as a key and a callable as value.
    
    Both in alphabetical order.
    """
    
    arg_dict = {}
    call_dict = {}
    
    for name, obj in inspect.getmembers(Module, inspect.isfunction):
        if name.startswith("_") or name.startswith("x"):
            continue

        sig = inspect.signature(obj)
        param_count = sum(1 for p in sig.parameters.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))

        if name not in arg_dict:
            arg_dict[name] = set()
        
        arg_dict[name].add(param_count)
        call_dict[name] = obj
    
    return arg_dict, call_dict

UNIFLIGHTARGMAP, UNIFLIGHTCALLMAP = _generateDicts(uniflight)
UNISPACEARGMAP,  UNISPACECALLMAP  = _generateDicts(unispace)
UNIPOWERARGMAP,  UNIPOWERCALLMAP  = _generateDicts(unipower)
UNICRYPTARGMAP,  UNICRYPTCALLMAP  = _generateDicts(unicrypt)
UNIPHYSARGMAP,   UNIPHYSCALLMAP   = _generateDicts(mechanics)
UNIMATHARGMAP,   UNIMATHCALLMAP   = _generateDicts(unimath)
UNIALGOARGMAP,   UNIALGOCALLMAP   = _generateDicts(unialgo)
