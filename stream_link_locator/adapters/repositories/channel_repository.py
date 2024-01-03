from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, Optional, List

from stream_link_locator.domain.models import Channel

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class ChannelAbstractRepository(ABC):
    """Channel Abstract Repository"""

    def __init__(self):
        self.seen: Set["Channel"] = set()

    def add(self, channel: "Channel"):
        """Add a boardgame to the repository"""
        self._add(channel)
        self.seen.add(channel)

    def get(self, channel_id: int) -> Optional["Channel"]:
        """Get a channel by its id"""
        channel = self._get(channel_id)
        if channel:
            self.seen.add(channel)
        return channel

    def get_by_name(self, name: str) -> Optional["Channel"]:
        """Get a channel by its name"""
        channel = self._get_by_name(name)
        if channel:
            self.seen.add(channel)
        return channel

    def get_all(self) -> List["Channel"]:
        """Get all channels"""
        channels = self._get_all()
        if channels:
            self.seen.update(channels)
        return channels

    @abstractmethod
    def _add(self, channel: "Channel"):
        raise NotImplementedError

    @abstractmethod
    def _get(self, channel_id: int) -> "Channel":
        raise NotImplementedError

    @abstractmethod
    def _get_by_name(self, name: str) -> "Channel":
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> List["Channel"]:
        raise NotImplementedError


class ChannelSqlAlchemyRepository(ChannelAbstractRepository):
    """Channel SQLAlchemy Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def _add(self, channel: "Channel"):
        self._session.add(channel)

    def _get(self, channel_id: int) -> Optional["Channel"]:
        return self._session.query(Channel).filter_by(id=channel_id).first()

    def _get_by_name(self, name: str) -> Optional["Channel"]:
        return self._session.query(Channel).filter_by(name=name).first()

    def _get_all(self) -> List["Channel"]:
        return self._session.query(Channel).all()
