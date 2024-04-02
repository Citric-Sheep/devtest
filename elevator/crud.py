"""
CRUD operations for elevator entities.
"""

from datetime import datetime, timedelta

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from elevator.model import ElevatorDb, ElevatorDemandDb

# Some CRUD operations


def create_elevator(session: Session, elevator: ElevatorDb) -> ElevatorDb:
    session.add(elevator)
    session.commit()
    session.refresh(elevator)
    return elevator


def create_elevator_demand(session: Session, elevator_demand: ElevatorDemandDb) -> ElevatorDemandDb:
    session.add(elevator_demand)
    session.commit()
    session.refresh(elevator_demand)
    return elevator_demand


def get_elevator(session: Session, elevator_id: int) -> ElevatorDb | None:
    return session.query(ElevatorDb).filter(ElevatorDb.id == elevator_id).first()


def get_elevators(session: Session, skip: int = 0, limit: int = 5) -> list[ElevatorDb]:
    return session.query(ElevatorDb).offset(skip).limit(limit).all()


def get_latest_elevator_demands(
    session: Session, skip: int = 0, limit: int = 15
) -> list[ElevatorDemandDb]:
    return (
        session.query(ElevatorDemandDb)
        .order_by(ElevatorDemandDb.requested_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_elevator_name(session: Session, elevator_id: int, name: str) -> ElevatorDb | None:
    elevator = session.query(ElevatorDb).filter(ElevatorDb.id == elevator_id).first()
    if elevator:
        elevator.name = name
        session.commit()
        session.refresh(elevator)
    return elevator


def delete_elevator(session: Session, elevator_id: int) -> None:
    elevator = session.query(ElevatorDb).filter(ElevatorDb.id == elevator_id).first()
    if elevator:
        session.delete(elevator)
        session.commit()


def top_floor_demand(session: Session, time_window: int = 10, use_dow: bool = False) -> int | None:
    """
    Searches historically for the floor that called the elevator the most within a specified time
    range around the current time, optionally filtering by the day of the week.

    :param session: DB session.
    :param time_window: Time window for filtering, in minutes.
    :param use_dow: Whether to filter demands by the current day of the week.
    :return: The floor most likely to demand the elevator, based on historical data.
    """
    now = datetime.utcnow()
    start_time = (now - timedelta(minutes=time_window)).time()
    end_time = (now + timedelta(minutes=time_window)).time()

    query = session.query(
        ElevatorDemandDb.pressed_at_floor,
        func.count(ElevatorDemandDb.pressed_at_floor),
    ).filter(
        func.time(ElevatorDemandDb.requested_at) >= start_time.strftime("%H:%M:%S"),
        func.time(ElevatorDemandDb.requested_at) <= end_time.strftime("%H:%M:%S"),
    )

    if use_dow:
        # `isoweekday` returns from 1-7 (Monday==1) and DB from 0-6 (Sunday==0)
        current_dow = now.isoweekday() % 7
        query = query.filter(extract("dow", ElevatorDemandDb.requested_at) == current_dow)

    top_floor = (
        query.group_by(ElevatorDemandDb.pressed_at_floor)
        .order_by(func.count(ElevatorDemandDb.pressed_at_floor).desc())
        .first()
    )

    return top_floor.pressed_at_floor if top_floor else None


# Business rules


def top_floor_demand_by_time(session: Session, time_window: int = 10) -> int | None:
    """
    Get the floor most likely to demand the elevator based on the historical data. This grabs the
    floor with the most frequency of demands around the current time.
    """
    return top_floor_demand(session, time_window, use_dow=False)


def top_floor_demand_by_time_and_dow(session: Session, time_window: int = 10) -> int | None:
    """
    Get the floor most likely to demand the elevator based on the historical data. This grabs the
    floor with the most frequency of demands around the current time and the current day of week.
    """
    return top_floor_demand(session, time_window, use_dow=True)
