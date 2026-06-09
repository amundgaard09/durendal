
from dataclasses import dataclass

@dataclass 
class MCPProperty:
    name: str
    ptype: type
    enum: type
    default: type
    desc: str