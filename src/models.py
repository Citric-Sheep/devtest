from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ElevatorCall(Base):
    """Represents an elevator call entitiy to be stored in a database.

        id (int): Unique identifier for the elevator.
        current_floor (int): The current floor of the elevator.
        destination_floor (int): Indicates the target floor to move the elevator.
        timestamp (datetime): Timestamp indicating when the elevator call was performed.
    """
    __tablename__ = 'elevator_calls'
    id = Column(Integer, primary_key=True)
    current_floor = Column(Integer)
    user_floor = Column(Integer)
    target_floor = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<ElevatorCall(id={self.id}, current_floor={self.current_floor}, user_floor={self.user_floor}, target_floor={self.target_floor}, timestamp={self.timestamp})>"


DATABASE_URL = "sqlite:///./elevator.db?check_same_thread=False"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine)

# Create tables
Base.metadata.create_all(engine)


def get_db():
    """Provides a database session. It ensures that the database session is properly 
    closed when the function execution is complete working as a context manager.

    Yields:
        Session: Database session 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
