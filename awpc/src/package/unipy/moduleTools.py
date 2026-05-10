"""Module for various data extraction tasks on modules in Python. Built on top of the `inspect` library"""

import inspect

from awpc.src.package.unipy.uniflight import uniflight
from awpc.src.package.unipy.unispace import unispace
from awpc.src.package.unipy.unicrypt import unicrypt
from awpc.src.package.unipy.unipower import unipower
from awpc.src.package.unipy.uniphys import uniphys
from awpc.src.package.unipy.unimath import unimath
from awpc.src.package.unipy.unialgo import unialgo

def _generateDicts(Module) -> tuple[dict, dict]:
    """Generate an argument count dict and function call dict for a module. Returns `(arg_count_dict, call_dict)`, both in alphabetical order."""
    
    arg_count_dict = {}
    call_dict = {}
    
    for name, obj in inspect.getmembers(Module, inspect.isfunction):
    
        if name.startswith("_") or name.startswith("x"):
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

UNIFLIGHTARGMAP, UNIFLIGHTCALLMAP = _generateDicts(uniflight)
UNISPACEARGMAP,  UNISPACECALLMAP  = _generateDicts(unispace)
UNIPOWERARGMAP,  UNIPOWERCALLMAP  = _generateDicts(unipower)
UNICRYPTARGMAP,  UNICRYPTCALLMAP  = _generateDicts(unicrypt)
UNIPHYSARGMAP,   UNIPHYSCALLMAP   = _generateDicts(uniphys)
UNIMATHARGMAP,   UNIMATHCALLMAP   = _generateDicts(unimath)
UNIALGOARGMAP,   UNIALGOCALLMAP   = _generateDicts(unialgo)
