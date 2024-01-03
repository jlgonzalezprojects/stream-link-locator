import logging

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    event,
)
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.exc import UnmappedError
from sqlalchemy.orm import registry

from stream_link_locator.domain.models import Channel

logger = logging.getLogger(__name__)

metadata = MetaData()
mapper_registry = registry()


channel_table = Table(
    "channels",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(250), nullable=False),
    Column("url", String(250), nullable=False),
)


def start_mappers():
    """Start ORM mappers with the domain model classes."""
    logger.info("Starting ORM mappers")
    if not exist_mapper(Channel):
        mapper_registry.map_imperatively(Channel, channel_table)


@event.listens_for(Channel, "load")
def channel_load(channel: "Channel", _):
    """Add events to channel after loading from database."""
    channel.events = []


def exist_mapper(klass) -> bool:
    """Check if the ORM mappers have been started."""
    try:
        class_mapper(klass)
        return True
    except UnmappedError:
        return False
