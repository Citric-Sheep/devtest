"""Service Layer"""

from typing import List

import numpy

from core.elevator.model import Demand, Elevator, Floor


def generate_demand(top: int, qty: int) -> List[Demand]:
    """Generate a list of random origin and destination floors."""
    return [
        Demand(origin=x, destination=y)
        for x, y in numpy.random.default_rng().integers(top, size=(qty, 2))
    ]


def run_simulation(top_floor: int, sample_size: int) -> None:
    """Execute Elevator simulation"""
    elevator = Elevator(
        top=Floor(top_floor), queue=generate_demand(top=top_floor, qty=sample_size)
    )
    elevator.run()
