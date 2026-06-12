
from pathlib import Path
from Icarus.core.mcp.types.input_schema import InputSchema
from dataclasses import dataclass

@dataclass
class MCPTool:
    name: str
    desc: str
    path: Path
    config: dict
    input_schema: InputSchema