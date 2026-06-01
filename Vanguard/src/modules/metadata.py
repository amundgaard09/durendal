
class Metadata:
    """Metadata class for storing metadata about an `Article` instance."""
    def __init__(
        self, 
        source: str, 
        url: str, 
        word_count: int, 
        saved_at: str, 
        link_count: int, 
        language: str
    ):
        self.source = source
        self.url = url
        self.word_count = word_count
        self.saved_at = saved_at
        self.link_count = link_count
        self.language = language
        
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "url": self.url,
            "word_count": self.word_count,
            "saved_at": self.saved_at,
            "link_count": self.link_count,
            "language": self.language
        }
            