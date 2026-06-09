
import os, json
from pathlib import Path
from types.mcptool import MCPTool
from types.input_schema import InputSchema

_SKILLS_DIR = r"C:\Users\Administrator\.vscode\durendal\Icarus\skills"

def create_input_schema() -> InputSchema:
    """Create a new MCPTool instance from a skill."""

def get_tools() -> list[MCPTool]:
    """Iterates through the skills directory and creates a list of MCPTools"""
    
    tools: list[MCPTool] = []
    
    for folder in os.listdir(_SKILLS_DIR):
        config_path = os.path.join(_SKILLS_DIR, folder, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                
                tools.append(MCPTool(
                    name="",
                    desc="",
                    path=Path(os.path.join(_SKILLS_DIR, folder)),
                    config=config,
                    input_schema={
                        
                    }
                ))
            