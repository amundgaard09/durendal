
from typing import Any
import importlib.util, json
from pathlib import Path
from core.utilities.decorators import logger

@logger
def get_py_skill_and_triggers(path: Path):
    py_path = path / "execute.py"
    json_path = path / "config.json"

    spec = importlib.util.spec_from_file_location(
        "skill_module",
        py_path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    with open(json_path, mode="r", encoding="utf-8") as f:
        jsondict: dict = json.load(f)
   
    triggers = jsondict.get("triggers", None)

    return module, triggers
