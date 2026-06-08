
from pathlib import Path
from .metadata import Metadata
from dataclasses import dataclass

@dataclass
class Article:
    """
    Article class representing a Wikipedia article, containing its name, ID, title, content path, links, and metadata.
    
    This is only a wrapper used to make indexing and retrieval easier, and to enable lazy loading. 
    The actual content is saved as a path to a Markdown file, and the links are stored as a list of `Link` objects.
    """ 
    name: str
    idstr: str 
    title: str 
    contentpath: Path
    links: list[tuple[str, str]]
    metadata: Metadata
    
        
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "idstr": self.idstr,
            "title": self.title,
            "content": str(self.contentpath),
            "links": [link for link in self.links],
            "metadata": self.metadata.to_dict()
        }
