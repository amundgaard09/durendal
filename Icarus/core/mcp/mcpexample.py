
import os, mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

server = Server("icarus-skill-engine")

SKILLS_DIR = r"C:\Users\Administrator\.vscode\durendal\Icarus\skills"

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """Exposes SKILL.md and subfolder readmes to ICARUS."""
    resources = [
        types.Resource(
            uri="skills://index",
            name="ICARUS Master Skill Index",
            mimeType="text/markdown",
            description="The primary SKILL.md file listing all assistant capabilities."
        )
    ]
    return resources

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Reads the content of the master SKILL.md file."""
    if uri == "skills://index":
        with open(os.path.join(SKILLS_DIR, "SKILL.md"), "r") as f:
            return f.read()
    raise ValueError(ResourceNotFound)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Dynamically converts skill subfolders into executable AI tools."""
    return [
        types.Tool(
            name="run_cad_analysis",
            description="Executes engineering analysis based on skills/cad_analysis definition.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the CAD file"},
                    "tolerance": {"type": "number", "default": 0.001}
                },
                "required": ["file_path"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Executes the actual engineering script inside the skill subfolder."""
    if name == "run_cad_analysis":
        # Put your actual local engineering script execution logic here
        file_path = arguments.get("file_path")
        return [types.TextContent(type="text", text=f"Successfully analyzed {file_path}")]
    raise ValueError(ToolNotFound)
