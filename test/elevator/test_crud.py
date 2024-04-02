"""
Tests for CRUD module.
"""

from datetime import datetime

import pytest
from freezegun import freeze_time
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from elevator import crud
from elevator.model import ElevatorDb, ElevatorDemandDb


@pytest.mark.parametrize(
    "elevators, elevator_id, expected_elevator",
    [
        (
            [
                ElevatorDb(id=1, name="south"),
                ElevatorDb(id=2, name="north"),
                ElevatorDb(id=3, name="west"),
            ],
            3,
            ElevatorDb(id=3, name="west"),
        ),
    ],
)
def test_get_elevator(
    elevators: list[ElevatorDb],
    elevator_id: int,
    expected_elevator: ElevatorDb,
    db_session: Session,
) -> None:
    for e in elevators:
        crud.create_elevator(db_session, e)
    actual_elevator = crud.get_elevator(db_session, elevator_id)
    assert actual_elevator.id == expected_elevator.id
    assert actual_elevator.name == expected_elevator.name


def test_get_latest_elevator_demands(db_session: Session) -> None:
    # Add test data to the DB
    elevator_demand = [
        ElevatorDemandDb(
            elevator_id=1, requested_at=datetime(2025, 1, 1, 12, 0), pressed_at_floor=1
        ),
        ElevatorDemandDb(
            elevator_id=1, requested_at=datetime(2025, 1, 1, 12, 5), pressed_at_floor=2
        ),
    ]
    for demand in elevator_demand:
        crud.create_elevator_demand(db_session, demand)
    # Call actual function
    latest_demands = crud.get_latest_elevator_demands(db_session, skip=0, limit=5)
    # Check the demands match added ones
    assert len(latest_demands) == 2
    assert latest_demands[0].pressed_at_floor == elevator_demand[1].pressed_at_floor


def test_delete_elevator(db_session: Session) -> None:
    # Add test data to the DB
    elevator = ElevatorDb(name="test_elevator")
    crud.create_elevator(db_session, elevator)
    crud.create_elevator_demand(
        db_session,
        ElevatorDemandDb(
            elevator_id=elevator.id, requested_at=datetime.utcnow(), pressed_at_floor=1
        ),
    )
    # Delete the elevator
    crud.delete_elevator(db_session, elevator.id)
    # There shouldn't be elevators nor demands
    remaining_demands = db_session.scalar(select(func.count()).select_from(ElevatorDemandDb))
    remaining_elevators = db_session.scalar(select(func.count()).select_from(ElevatorDb))
    assert remaining_demands == 0
    assert remaining_elevators == 0


@pytest.mark.parametrize(
    "elevator, current_time, elevator_demands, time_window, expected_result",
    [
        # In this case, historically - near the current frozen time, the most frequent pressed
        # floor was the 1st floor
        (
            ElevatorDb(id=1, name="south"),
            "2025-09-11 20:00:00",
            [
                ElevatorDemandDb(
                    elevator_id=1,
                    requested_at=datetime(2025, 9, 11, 19, 55),
                    pressed_at_floor=1,
                ),
                ElevatorDemandDb(
                    elevator_id=1,
                    requested_at=datetime(2025, 9, 11, 20, 0),
                    pressed_at_floor=2,
                ),
                ElevatorDemandDb(
                    elevator_id=1,
                    requested_at=datetime(2025, 9, 11, 20, 0),
                    pressed_at_floor=1,
                ),
                ElevatorDemandDb(
                    elevator_id=1,
                    requested_at=datetime(2025, 9, 11, 20, 5),
                    pressed_at_floor=3,
                ),
            ],
            10,
            1,
        ),
        # There is no historical data for the time range, it should return None.
        (
            ElevatorDb(id=2, name="north"),
            "2025-10-11 20:00:00",
            [],
            10,
            None,
        ),
    ],
)
def test_top_floor_demand_by_time(
    db_session: Session,
    elevator: ElevatorDb,
    current_time: str | datetime,
    elevator_demands: list[ElevatorDemandDb],
    time_window: int,
    expected_result: int | None,
):
    # Add test data to the DB
    crud.create_elevator(db_session, elevator)
    for elevator_demand in elevator_demands:
        crud.create_elevator_demand(db_session, elevator_demand)
    # Call the actual function with frozen time
    with freeze_time(current_time):
        actual_result = crud.top_floor_demand_by_time(db_session, time_window)
    # Check results
    assert actual_result == expected_result


@pytest.mark.parametrize(
    "elevator, current_time, elevator_demands, time_window, expected_result",
    [
        # In this case elevator was called more frequently in 3rd floor near 20:00 hours,
        # but since current (frozen) day-of-week is a Friday, we consider that date.
        # This should return 4.
        (
            ElevatorDb(id=1, name="west"),
            # Friday
            "2025-09-12 20:00:00",
            [
                ElevatorDemandDb(
                    elevator_id=1,
                    # Friday
                    requested_at=datetime(2025, 9, 12, 19, 55),
                    pressed_at_floor=4,
                ),
                ElevatorDemandDb(
                    elevator_id=1,
                    # Thursday
                    requested_at=datetime(2025, 9, 11, 20, 5),
                    pressed_at_floor=3,
                ),
                ElevatorDemandDb(
                    elevator_id=1,
                    # Monday
                    requested_at=datetime(2025, 9, 8, 19, 58),
                    pressed_at_floor=3,
                ),
            ],
            10,
            4,
        ),
        # There is no historical data for Tuesday, should return None.
        (
            ElevatorDb(id=2, name="east"),
            # Tuesday
            "2025-11-11 20:00:00",
            [
                ElevatorDemandDb(
                    elevator_id=1,
                    # Monday
                    requested_at=datetime(2025, 11, 9, 19, 56),
                    pressed_at_floor=3,
                )
            ],
            20,
            None,
        ),
    ],
)
def test_top_floor_demand_by_time_and_dow(
    db_session: Session,
    elevator: ElevatorDb,
    current_time: str | datetime,
    elevator_demands: list[ElevatorDemandDb],
    time_window: int,
    expected_result: int | None,
):
    # Add test data to the DB
    crud.create_elevator(db_session, elevator)
    for elevator_demand in elevator_demands:
        crud.create_elevator_demand(db_session, elevator_demand)
    # Call the actual function with frozen time
    with freeze_time(current_time):
        actual_result = crud.top_floor_demand_by_time_and_dow(db_session, time_window)
    # Check results
    assert actual_result == expected_result
