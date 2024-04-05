"""Models"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, NewType


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s"
)

Floor = NewType("Floor", int)


@dataclass
class Demand:
    """Demand is considered a user's request to use the elevator"""

    origin: Floor
    destination: Floor
    user_qty: int = 1


class Elevator(ABC):
    """Elevator simulation model"""

    def __init__(self: "Elevator"):
        """Init function for Elevator class"""

    @abstractmethod
    def _open_doors(self: "Elevator") -> None:
        """Time it takes the elevator to open doors"""
        raise NotImplementedError

    def _close_doors(self: "Elevator") -> None:
        """Time it takes the elevator to open doors"""
        raise NotImplementedError

    def _move_to(self: "Elevator", floor: Floor) -> None:
        """Elevator movement"""
        raise NotImplementedError

    def attend(self: "Elevator", demand: Demand) -> None:
        """Attend an elevator request (demand)."""
        raise NotImplementedError

    def register(self: "Elevator", demand: Demand):
        """Register demand in queue"""
        raise NotImplementedError

    def update_queue(self: "Elevator", queue: List[Demand]):
        """Update elevator queue by adding demand"""
        raise NotImplementedError

    def run(self):
        """Turn ON the elevator"""
        raise NotImplementedError
