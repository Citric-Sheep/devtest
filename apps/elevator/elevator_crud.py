##############
# Libraries #
##############
import json

from sqlalchemy import asc
from sqlalchemy.orm import Session

from apps.elevator.elevator_utilities import Elevator
from database.db_models import ElevatorOrders, Elevators

from apps.elevator.elevator_schemas import ElevatorCheck, ElevatorDemand, ElevatorUpdate, ElevatorStatus
from apps.elevator.elevator_exceptions import DatabaseError


###############################
# Add demand to the database #
###############################

def add_demand(demand_info: ElevatorDemand,
               db_session: Session):
    try:
        demand_data = ElevatorOrders(elevator_id=demand_info.elevator_id,
                                     elevator_order_demand_category=demand_info.demand_category,
                                     elevator_order_demand_type=demand_info.demand_type,
                                     elevator_order_current_floor=demand_info.current_floor,
                                     elevator_order_demand_floor=demand_info.destination_floor,
                                     elevator_order_movement_status=demand_info.current_movement
                                     )

        db_session.add(demand_data)
        db_session.commit()
        db_session.refresh(demand_data)

        qJson = db_session.query(Elevators) \
            .filter(Elevators.elevator_id == demand_info.elevator_id).first().elevators_request_queue

        q = json.loads(qJson)
        q.append(demand_data.elevator_order_id)

        db_session.query(Elevators) \
            .filter(Elevators.elevator_id == demand_info.elevator_id) \
            .update({"elevators_request_queue": json.dumps(q)})

        db_session.commit()

    except Exception as error:
        db_session.rollback()
        raise DatabaseError(message="There was an unexpected error while adding to the database",
                            original_exception=error)


####################
# add status data #
####################

def add_status(status_info: ElevatorStatus,
               db_session: Session):
    try:
        status_data = ElevatorOrders(elevator_id=status_info.elevator_id,
                                     elevator_status_movement=status_info.current_movement,
                                     elevator_status_current_floor=status_info.current_floor,
                                     elevator_status_destination_floor=status_info.destination_floor)
        db_session.add(status_data)
        db_session.commit()
        db_session.refresh(status_data)
    except Exception as error:
        db_session.rollback()
        raise DatabaseError(message="There was an unexpected error while adding to the database",
                            original_exception=error)


##########################
# Check current demands #
##########################

def check_demand(demand_info: ElevatorCheck,
                 db_session: Session):
    try:
        qJson = db_session.query(Elevators) \
            .filter(Elevators.elevator_id == demand_info.elevator_id).first().elevators_request_queue
        q = json.loads(qJson)

        reqs = db_session.query(ElevatorOrders).filter(ElevatorOrders.elevator_order_id.in_(q)).all()

        elevator = Elevator(request_queue=reqs,
                            direction=demand_info.current_movement,
                            current_floor=demand_info.current_floor)
        elevator_demand = elevator.target_floor()
        return elevator_demand
    except Exception as error:
        raise DatabaseError(message="There was an unexpected error while checking the current demands",
                            original_exception=error)


###########################
# Update current demands #
###########################

def update_demands(update_info: ElevatorUpdate,
                   db_session: Session):
    try:
        qJson = db_session.query(Elevators) \
            .filter(Elevators.elevator_id == update_info.elevator_id).first().elevators_request_queue

        q = json.loads(qJson)
        q.remove(update_info.request_id)

        db_session.query(Elevators) \
            .filter(Elevators.elevator_id == update_info.elevator_id) \
            .update({"elevators_request_queue": json.dumps(q)})

        db_session.commit()
    except Exception as error:
        db_session.rollback()
        raise DatabaseError(message="There was an unexpected error while updating the database",
                            original_exception=error)
