from dataclasses import dataclass, field

from .aggregate import Aggregate


@dataclass
class Channel(Aggregate):
    """Channel class"""

    id: int = field(init=False)
    name: str = ""
    url: str = ""

    def __hash__(self):
        return hash(f"{self.name}-{self.url}")

    def __repr__(self):
        return f"Channel({self.name}, {self.url})"
