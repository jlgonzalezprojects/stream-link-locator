from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from config import settings

from stream_link_locator.adapters.repositories import ChannelAbstractRepository, ChannelSqlAlchemyRepository


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work"""

    def __init__(self):
        self.channels: Optional["ChannelAbstractRepository"] = None
        self.engine = None

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_events(self):
        """Collect new events from channels"""
        for channel in self.channels.seen:
            while channel.events:
                yield channel.events.pop(0)

    @abstractmethod
    def commit(self):
        """Commit the unit of work"""
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        """Rollback the unit of work"""
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(
            f"postgresql://{settings.database.user}:{settings.database.password}"
            f"@{settings.database.host}:{settings.database.port}/{settings.database.database}",
            isolation_level="REPEATABLE READ",
        )
        self.session_factory = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session: "Session" = self.session_factory()
        self.channels = ChannelSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
