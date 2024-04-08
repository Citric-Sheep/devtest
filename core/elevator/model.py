"""Elevator domain model"""

import logging
from dataclasses import dataclass
from time import sleep
from typing import List, NewType, Optional, Union

from core.elevator.constants import ElevatorStatus, ElevatorTiming

Floor = NewType("Floor", int)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s :: %(levelname)s :: %(message)s"
)


@dataclass
class Demand:
    """Demand is considered a user's request to use the elevator"""

    origin: Floor
    destination: Floor


class Elevator:
    """Elevator Model"""

    def __init__(
        self: "Elevator",
        top: Union[Floor, int],
        current: Union[Floor, int] = 0,
        queue: Optional[List[Demand]] = None,
    ):
        """Init function for Elevator class"""
        super().__init__()
        self.top = Floor(top)
        self.current = Floor(current)
        self.queue = queue if queue else []
        self.status: ElevatorStatus = ElevatorStatus.VACANT
        self.is_opened: bool = False

    def _open_doors(self: "Elevator") -> None:
        """Time it takes the elevator to open doors"""
        if not self.is_opened:
            logging.debug("Doors opening.")
            self.is_opened = True
            sleep(ElevatorTiming.OPEN)

    def _close_doors(self: "Elevator") -> None:
        """Time it takes the elevator to open doors"""
        if self.is_opened:
            logging.debug("Doors closing.")
            sleep(ElevatorTiming.CLOSE)
            self.is_opened = False

    def _move_to(self: "Elevator", floor: Floor) -> None:
        """Elevator movement"""
        self._close_doors()
        logging.debug("Current floor: %s", self.current)
        while floor != self.current:
            self.current += 1 if floor > self.current else -1
            sleep(ElevatorTiming.PER_FLOOR)
            logging.debug("Current floor: %s", self.current)

    def attend(self: "Elevator", demand: Demand) -> None:
        """Attend an elevator request (demand)."""
        if demand.origin == demand.destination:
            logging.debug("Demand origin is same as destination.")
            return
        logging.info("Preparing to ATTEND %s", demand)
        self.status = ElevatorStatus.BUSY
        logging.info("Status: %s", self.status)
        if demand.origin != self.current:
            self._move_to(floor=demand.origin)
        self._open_doors()
        sleep(ElevatorTiming.WAIT_PASSENGERS)
        self._move_to(floor=demand.destination)
        self._open_doors()
        sleep(ElevatorTiming.WAIT_PASSENGERS)
        self._close_doors()

    def run(self: "Elevator"):
        """Turn ON the elevator"""
        self.status = ElevatorStatus.BUSY
        for demand in self.queue:
            self.attend(demand=demand)
        self.status = ElevatorStatus.VACANT
        logging.info("Status: %s", self.status)
