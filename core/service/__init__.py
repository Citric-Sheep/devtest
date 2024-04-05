"""Service Layer"""

import logging
from time import sleep
from typing import List, Optional

from core.elevator.constants import ElevatorStatus, ElevatorTiming
from core.elevator.errors import ElevatorError
from core.elevator.model import Demand, Elevator, Floor


def _wait_users(qty: int) -> None:
    """Time it takes the users to enter/leave the elevator"""
    if qty <= 0:
        raise ElevatorError("User quantity must be at least 1.")
    logging.info("Users (%s) passing.", qty)
    sleep(ElevatorTiming.PER_USER_TO_PASS * qty)


class ElevatorService(Elevator):
    """Elevator simulation model"""

    def __init__(
        self: "ElevatorService",
        top: Floor,
        current: Floor = Floor(0),
        queue: Optional[List[Demand]] = None,
    ):
        """Init function for Elevator class"""
        super().__init__()
        self.top = top
        self.current = current
        self.queue = queue if queue else []
        self.status: ElevatorStatus = ElevatorStatus.VACANT
        self.is_opened: bool = False

    def _open_doors(self: "ElevatorService") -> None:
        """Time it takes the elevator to open doors"""
        if not self.is_opened:
            logging.debug("Doors opening.")
            self.is_opened = True
            sleep(ElevatorTiming.OPEN)

    def _close_doors(self: "ElevatorService") -> None:
        """Time it takes the elevator to open doors"""
        if self.is_opened:
            logging.debug("Doors closing.")
            sleep(ElevatorTiming.CLOSE)
            self.is_opened = False

    def _move_to(self: "ElevatorService", floor: Floor) -> None:
        """Elevator movement"""
        logging.info("Preparing trip to %s", floor)
        self._close_doors()
        logging.debug("Current floor: %s", self.current)
        while floor != self.current:
            self.current += 1 if floor > self.current else -1
            sleep(ElevatorTiming.PER_FLOOR)
            logging.debug("Current floor: %s", self.current)

    def attend(self: "ElevatorService", demand: Demand) -> None:
        """Attend an elevator request (demand)."""
        logging.info("Preparing to ATTEND %s", demand)
        self.status = ElevatorStatus.BUSY
        if demand.origin != self.current:
            self._move_to(floor=demand.origin)
        self._open_doors()
        _wait_users(qty=demand.user_qty)
        self._move_to(floor=demand.destination)
        self._open_doors()
        _wait_users(qty=demand.user_qty)
        self._close_doors()

    def register(self: "ElevatorService", demand: Demand):
        """Register demand in queue or attend if queue is empty"""
        # TODO: Validate demand by applying domain rules
        if self.status == ElevatorStatus.BUSY:
            # Case1: Elevator is busy -> Append to line
            self.queue.append(demand)
        if self.status == ElevatorStatus.VACANT:
            # Case3: Queue is empty, elevator is vacant
            self.attend(demand)

    def update_queue(self: "ElevatorService", queue: List[Demand]):
        """Update elevator queue by adding demand"""
        self.queue = queue

    def run(self: "ElevatorService"):
        """Turn ON the elevator"""
        self.status = ElevatorStatus.BUSY
        for demand in self.queue:
            self.attend(demand=demand)
        self.status = ElevatorStatus.VACANT
        logging.info("Status: %s", ElevatorStatus.VACANT)
