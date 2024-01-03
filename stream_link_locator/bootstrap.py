import logging
from logging import Logger

from stream_link_locator.adapters import orm
from stream_link_locator.domain.commands import LoadChannels
from stream_link_locator.domain.events import ChannelCreated, ChannelUrlUpdated
from stream_link_locator.services.loader_service import LoaderService
from stream_link_locator.services.message_bus import MessageBus
from stream_link_locator.services.unit_of_work import (
    AbstractUnitOfWork,
    SqlAlchemyUnitOfWork,
)


def bootstrap(
    start_orm: bool = True,
    uow: "AbstractUnitOfWork" = SqlAlchemyUnitOfWork(),
    logger: "Logger" = logging.getLogger(__name__),
) -> MessageBus:
    """Bootstrap the application"""
    if start_orm:
        orm.start_mappers()
        orm.metadata.create_all(uow.engine)
    injected_event_handlers = {
        ChannelCreated: [lambda e: logger.info(e)],
        ChannelUrlUpdated: [lambda e: logger.info(e)],
    }
    injected_command_handlers = {LoadChannels: LoaderService(logger, uow)}
    return MessageBus(uow, injected_event_handlers, injected_command_handlers)
