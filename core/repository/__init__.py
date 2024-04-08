"""Repository layer"""
import logging
from abc import ABC, abstractmethod
from pprint import pformat
from typing import Any, List, Optional, Type

from sqlalchemy import CursorResult, delete
from sqlalchemy.orm.session import Session

from core.repository.orm import Record


class AbstractRepository(ABC):
    """Abstract Repository Class"""

    @abstractmethod
    def create(self, records):
        """Create records"""
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        """Lists records"""
        raise NotImplementedError

    @abstractmethod
    def get_item(self, record_id):
        """Get record by ID"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, record_id):
        """Delete record"""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """Repository interface to interact with SQLAlchemy"""

    def __init__(self, session: Session) -> None:
        """Init function"""
        self.session = session

    def create(self, records: List[List[int]]) -> bool:
        """Insert records in database"""
        try:
            items = [Record(origin=item[0], destination=item[1]) for item in records]
            self.session.add_all(items)
        except Exception as ex:
            logging.error(pformat(ex))
            return False
        return True

    def get_item(self, record_id: int) -> Optional[Record]:
        """Get a record from database by ID"""
        return self.session.query(Record).filter_by(id=record_id).first()

    def get_all(self) -> list[Type[Record]]:
        """List all records from database"""
        try:
            return self.session.query(Record).all()
        except Exception as ex:
            logging.error(pformat(ex))

    def delete(self, record_id) -> CursorResult[Any]:
        """Delete a record from database"""
        return self.session.execute(delete(Record).where(Record.id == record_id))
