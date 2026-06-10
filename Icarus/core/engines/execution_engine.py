"""
The `ICARUS` Complex Execution Engine

This file contains dependencies for ICARUS linked to execution of commands and tasks.

---

The ICARUS Complex is a Durendal project. More information can be found at the [Durendal GitHub](https://github.com/amundgaard09/durendal/)
"""

import os
from pathlib import Path
from typing import Callable
from core.mcp.skill_loaders import get_py_skill_and_triggers

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

def normalize(string: str) -> str:
    return string.lower().strip()

def handle_unknown(string: str) -> str:
    return "I didn't understand that."

def match(text: str):
    text = normalize(text)

    for trigger in TRIGGERMAP:
        if trigger in text:
            return TRIGGERMAP[trigger]

    return None

def process(user_input: str):
    """The main Execution engine function for now."""
    func = match(user_input)
    
    if func is None:
        return handle_unknown(user_input)
    else:
        return func()


