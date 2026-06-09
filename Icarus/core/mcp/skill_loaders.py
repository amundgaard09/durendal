
import importlib.util
from pathlib import Path

def get_py_skill(path: Path):
    module_path = path / "execute.py"

    spec = importlib.util.spec_from_file_location(
        "skill_module",
        module_path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module
