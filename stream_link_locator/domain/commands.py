"""Commands module, this module contains all the channel commands."""
from dataclasses import dataclass
from typing import Optional


class Command:
    """Event base class"""

    pass


@dataclass
class LoadChannels(Command):
    """Load boardgame command"""

    source: Optional[str] = None

