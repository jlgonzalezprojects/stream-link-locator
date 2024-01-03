"""Events module, this module contains all the link locator events."""
from dataclasses import dataclass


class Event:
    """Event base class"""

    pass


@dataclass
class ChannelCreated(Event):
    """Channel created event"""

    name: str
    url: str


@dataclass
class ChannelUrlUpdated(Event):
    """Channel url updated event"""

    name: str
    previous_url: str
    url: str
