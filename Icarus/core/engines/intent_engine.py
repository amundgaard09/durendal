"""
The `ICARUS` Complex Intent Engine

This file contains dependencies for ICARUS linked to figuring out what and how to do tasks.

---

The ICARUS Complex is a Durendal project. More information can be found at the [Durendal GitHub](https://github.com/amundgaard09/durendal/)
"""

from durapy import uniCLI
from typing import Callable
from core.utilities.decorators import logger

def get_highest_score(scored_func_list: list[tuple[int, Callable[[], str]]]) -> Callable[[], str] | None:
    """Returns the highest scoring function in a scored function list."""
    if not scored_func_list:
        return None

    return max(scored_func_list, key=lambda item: item[0])[1]
        
def get_most_probable_function(tokens: list[str], token_map: dict[str, Callable[[], str]]) -> Callable[[], str]:
    pass

def match_rev2(query: str, token_map: dict[str, Callable[[], str]]) -> None:
    "Uses a score-based system for checking the prompt up against a token map, and the function whose tokens are most common in the prompt gets returned."
    
    tokens = [token for token in query.strip().split()]
    
    return get_most_probable_function(tokens, token_map)


def normalize(string: str) -> str:
    return string.lower().strip()

@logger
def match(query: str, trigger_map: dict) -> Callable[[], str] | None:
    """Extracts triggers from query and returns the most probable function."""
    query = normalize(query)

    for trigger in trigger_map: # Loop over all triggers (sentences) in the trigger map
        if trigger in query:
            return trigger_map[trigger] # Return function for given trigger

    return None

@logger
def initialize() -> None:
    uniCLI.console_print("ICARUS", "blue", "Initializing Icarus Intent Engine...", "white")
    