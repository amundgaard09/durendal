
from pathlib import Path
from link import Link

class Article:
    def __init__(
        self, 
        name: str, 
        id: str, 
        title: str, 
        contentpath: Path, 
        links: list[Link], 
        metadata: dict
    ):
        self.name = name
        self.id = id
        self.title = title
        self.content = contentpath
        self.links = links
        self.metadata = metadata
