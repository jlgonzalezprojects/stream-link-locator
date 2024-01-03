from enum import Enum, auto

from config import settings
from stream_link_locator.adapters.parsers.elcano_parser import ElCanoParser


class ParserType(Enum):
    """Parser types"""

    ELCANO = auto()

    @classmethod
    def from_name(cls, parser_name: str):
        """Get parser type from string"""
        for item in cls:
            if item.name.lower() == parser_name.lower():
                return item
        raise ValueError(f"Invalid parser name - {parser_name}")


def parser_factory(parser_type: ParserType):
    """Parser factory"""
    if parser_type == ParserType.ELCANO:
        return ElCanoParser(url=settings.parser.elcano_url)
    else:
        raise ValueError(f"Invalid parser type - {parser_type}")
