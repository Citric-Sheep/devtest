from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class ElevatorCall(Base):
    """Elevator call is a table in the database containing the information about the elevator's movements.

    Args:
        Base (_type_): _description_
    """

    __tablename__ = "elevator_calls"

    # With call_time and floor_number we can evaluate the specific times during the day where the elevator is mostly located and used
    id = Column(Integer, primary_key=True, index=True)
    call_time = Column(DateTime)
    floor_number = Column(Integer)
