
import time
from pathlib import Path
from durapy import uniCLI

STD_LOG_PATH = Path(__file__).resolve().parents[2] / "logs"
RUNTIME_LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "runtime_log.txt"
DEBUG_LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "debug_log.txt"

def log(content: str, path: Path = RUNTIME_LOG_PATH) -> bool:
    try:
        with open(path, mode="a", encoding="utf-8") as f:
            f.write(f"{time.strftime('<%H:%M:%S>')} - {content}")
            return True
    except Exception as e:
        uniCLI.console_print("LOGGER", "red", f"Error: {e}", "red")
        return False