from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from src.models import Elevator, Floor, Demand


class BaseRepository(ABC):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, model, obj_id):
        pass