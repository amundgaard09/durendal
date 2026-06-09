
from mcp_property import MCPProperty
from dataclasses import dataclass

@dataclass
class InputSchema:
    name: str
    desc: str
    IS_type: object
    properties: list[MCPProperty]
    required: list[str]
    schema = { # REMOVE THIS
        "inputSchema": {
            "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state/country, e.g., 'San Francisco, CA' or 'Tokyo, Japan'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "celsius",
                        "description": "The temperature unit to return."
                }
            },
            "required": ["location"]
        }
    }
