"""Constants module for elevator domain"""

from enum import Enum


class ElevatorStatus(str, Enum):
    """Status indicates whether the elevator is vacant or not"""

    VACANT = "vacant"
    BUSY = "busy"
    DISABLED = "disabled"


class ElevatorTiming(int, Enum):
    """Time it takes the elevator to perform some actions, in seconds"""

    OPEN = 0.5
    CLOSE = 0.8
    PER_FLOOR = 1.2
    PER_USER_TO_PASS = 1.5
