from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, id):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass

class DatabaseEntry(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass