"""Constants module for elevator domain"""

from enum import Enum


class ElevatorStatus(str, Enum):
    """Status indicates whether the elevator is vacant or not"""

    VACANT = "vacant"
    BUSY = "busy"
    DISABLED = "disabled"


class ElevatorTiming(int, Enum):
    """Time it takes the elevator to perform some actions, in seconds"""

    OPEN = 0.1
    CLOSE = 0.2
    PER_FLOOR = 0.3
    PER_USER_TO_PASS = 0.4
