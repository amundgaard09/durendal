
from pathlib import Path

class Link:
    def __init__(self, _from: Path, _to: Path):
        self._from = _from
        self._to = _to
    
    def to_dict(self) -> dict:
        return {
            "_from": str(self._from),
            "_to": str(self._to)    
        }