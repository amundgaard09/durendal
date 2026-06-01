
from pathlib import Path
from .link import Link
from .metadata import Metadata

class Article:
    """
    Article class representing a Wikipedia article, containing its name, ID, title, content path, links, and metadata.
    
    This is only a wrapper used to make indexing and retrieval easier, and to enable lazy loading. 
    The actual content is saved as a path to a Markdown file, and the links are stored as a list of `Link` objects.
    """
    def __init__(
        self, 
        name: str, 
        idstr: str, 
        title: str, 
        contentpath: Path, 
        links: list[Link], 
        metadata: Metadata
    ):
        self.name = name
        self.idstr = idstr
        self.title = title
        self.content = contentpath
        self.links = links
        self.metadata = metadata
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "idstr": self.idstr,
            "title": self.title,
            "content": str(self.content),
            "links": [link.to_dict() for link in self.links],
            "metadata": self.metadata.to_dict()
        }
