"""
The `ICARUS` Complex Execution Engine

This file contains dependencies for ICARUS linked to execution of commands and tasks.

---

The ICARUS Complex is a Durendal project. More information can be found at the [Durendal GitHub](https://github.com/amundgaard09/durendal/)
"""

import os
from pathlib import Path
from typing import Callable
from core.mcp.skill_loaders import get_py_skill_and_triggers, get_py_skill_and_tokens
from core.engines.intent_engine import match
from durapy import uniCLI

_ROOT  = Path(__file__).resolve().parents[2]
_SKILLS_DIR = _ROOT / "skills"

def isdunder(string: str) -> bool:
    return string.startswith("__") and string.endswith("__")

def build_triggermap() -> dict[str, Callable[[], str]]:
    """Builds the triggermap which is a dictionary that maps trigger phrases to a function."""
    
    map: dict = {}
    triggers: list[str]
    
    for folder in os.listdir(_SKILLS_DIR):
        if isdunder(folder):
            continue
        
        module, triggers = get_py_skill_and_triggers(_SKILLS_DIR / Path(folder))
        for trigger in triggers:
            if trigger in map:
                raise ValueError(f"Duplicate trigger: {trigger}")
            
            map[trigger.lower().strip()] = module.execute
    
    return map

TRIGGERMAP = build_triggermap()

def build_tokenmap() -> dict[list[str], Callable[[], str]]:
    """Builds the triggermap which is a dictionary that maps trigger phrases to a function."""
    
    map: dict = {}
    tokens: list[str]
    
    for folder in os.listdir(_SKILLS_DIR):
        if isdunder(folder):
            continue
        
        module, triggers = get_py_skill_and_tokens(_SKILLS_DIR / Path(folder))
        for trigger in triggers:
            if trigger in map:
                raise ValueError(f"Duplicate trigger: {trigger}")
            
            map[trigger.lower().strip()] = module.execute
    
    return map

def handle_unknown() -> str: # Add closest function system
    return "I didn't understand that."

def respond(user_input: str):
    """The main Execution engine function for now."""
    func = match(user_input, TRIGGERMAP)
    
    if func is None:
        return handle_unknown()
    else:
        return func()

def initialize() -> None:
    uniCLI.console_print("ICARUS", "blue", "Initializing Icarus Execution Engine...", "white")
    

