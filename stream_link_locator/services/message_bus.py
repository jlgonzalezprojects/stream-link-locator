import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING, Optional, Any

from stream_link_locator.domain.events import Event
from stream_link_locator.domain.commands import Command

if TYPE_CHECKING:
    from .unit_of_work import AbstractUnitOfWork

logger = logging.getLogger(__name__)

Message = Union[Command, Event]


class MessageBus:
    """Message bus class"""

    def __init__(
        self,
        uow: "AbstractUnitOfWork",
        event_handlers: Dict[Type[Event], List[Callable]],
        command_handlers: Dict[Type[Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: List[Message] = []

    def handle(self, message: Message) -> Optional[Any]:
        """Handle a message"""
        result = None
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Command):
                result = self.handle_command(message)
            else:
                raise RuntimeError(f"{message} is not an Event or Command")
        return result

    def handle_event(self, event: Event):
        """Handle an event"""
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug(f"Handling event {event} with handler {handler}")
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)

    def handle_command(self, command: Command):
        """Handle a command"""
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            result = handler(command)
            self.queue.extend(self.uow.collect_new_events())
            return result
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
