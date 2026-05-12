"""
This module provides helper functions and utilities for mathematics throughout the `AWPC` Library.
"""

def floatclip(val: float, lower: float, upper: float) -> int:
    if val <= lower:
        return lower
    elif val >= upper:
        return upper
    return val

def intclip(val: int, lower: int, upper: int) -> int:
    if val <= lower:
        return lower
    elif val >= upper:
        return upper
    return val