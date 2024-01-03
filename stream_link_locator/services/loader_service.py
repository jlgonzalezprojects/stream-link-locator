from logging import Logger
from typing import Optional

from stream_link_locator.adapters.parsers.parser_factory import (
    parser_factory,
    ParserType,
)
from stream_link_locator.domain.commands import LoadChannels
from stream_link_locator.domain.events import ChannelCreated, ChannelUrlUpdated
from stream_link_locator.services.unit_of_work import AbstractUnitOfWork


class LoaderService:
    """Service to load channels from a parser to the database"""

    def __init__(self, logger: Logger, uow: AbstractUnitOfWork):
        self._logger = logger
        self._uow = uow
        self._channel_parser = None

    def __call__(self, cmd: "LoadChannels"):
        self.set_parser(cmd.source)
        self._logger.info(f"Parsing channels from {self._channel_parser.url}...")
        with self._uow:
            parsed_channels = self._channel_parser.parse()
            for parsed_channel in parsed_channels:
                if channel := self._uow.channels.get_by_name(parsed_channel.name):
                    previous_url = channel.url
                    channel.url = parsed_channel.url
                    channel.events.append(
                        ChannelUrlUpdated(
                            name=channel.name,
                            url=channel.url,
                            previous_url=previous_url,
                        )
                    )
                else:
                    channel = parsed_channel
                    channel.events.append(
                        ChannelCreated(name=channel.name, url=channel.url)
                    )
                self._uow.channels.add(channel)
            self._uow.commit()

    def set_parser(self, source: Optional[str]):
        """Set the parser to use"""
        source = source or "elcano"
        self._channel_parser = parser_factory(ParserType.from_name(source))
        return self
