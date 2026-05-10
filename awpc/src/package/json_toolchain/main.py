"""
The `AWPC` `JSON` Toolchain module.
"""

def InsertJSON(PathToJSON: str, ContentDict: dict) -> None:
    """Inserts a dictionary into a `JSON` file. If the file does not exist, it creates it. Returns `True` if the operation was successful, `False` otherwise."""
    
    import json
    
    with open(PathToJSON, 'w') as JSONFile:
        json.dump(ContentDict, JSONFile, indent=4, sort_keys=True)
def ExtractJSON(PathToJSON: str) -> dict:
    """Extracts a `JSON` file and returns the content as a dictionary. Returns `None` if the file is not found or if there is an error during extraction."""
    
    import json
    
    try:
        with open(PathToJSON, 'r', encoding='utf-8') as file:
            return json.load(file)
        
    except Exception:
        return None