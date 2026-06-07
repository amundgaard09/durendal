
from dataclasses import dataclass

@dataclass
class Metadata:
    """Metadata class for storing metadata about an `Article` instance."""
    source: str
    """The source of the article."""
    url: str
    """The URL of the article."""
    word_count: int
    """The number of words in the article."""
    saved_at: str
    """The timestamp when the article was saved."""
    link_count: int
    """The number of links in the article."""
    language: str
    """The language of the article."""
     
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "url": self.url,
            "word_count": self.word_count,
            "saved_at": self.saved_at,
            "link_count": self.link_count,
            "language": self.language
        }
            