from abc import abstractmethod
from typing import List

from stream_link_locator.domain.models import Channel


class BaseParser:
    """Base parser class"""

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def parse(self) -> List[Channel]:
        """Parse the url and return a list of channels"""
        raise NotImplementedError
