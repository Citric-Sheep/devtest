##############
# Libraries #
##############

from sqlalchemy import asc
from sqlalchemy.orm import Session

from database.db_models import ElevatorOrders

from apps.elevator.elevator_schemas import ElevatorCheck, ElevatorDemand, ElevatorUpdate, ElevatorStatus, ElevatorDelete
from apps.elevator.elevator_utilities import Elevator
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
                                     elevator_order_movement_status=demand_info.current_movement,
                                     elevator_order_request_status=1)
        db_session.add(demand_data)
        db_session.commit()
        db_session.refresh(demand_data)
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
        records = db_session.query(ElevatorOrders).filter(ElevatorOrders.elevator_id == demand_info.elevator_id,
                                                          ElevatorOrders.elevator_order_request_status == 1)\
                            .order_by(asc(ElevatorOrders.elevator_order_update_on)).all()

        elevator = Elevator(request_queue=records,
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
        db_session.query(ElevatorOrders) \
                  .filter(ElevatorOrders.elevator_id == update_info.elevator_id,
                          ElevatorOrders.elevator_order_request_status == 1,
                          ElevatorOrders.elevator_order_demand_floor == update_info.current_floor,
                          ElevatorOrders.elevator_order_demand_category == 2) \
                .update({'elevator_order_request_status': 2})
        db_session.query(ElevatorOrders) \
                  .filter(ElevatorOrders.elevator_id == update_info.elevator_id,
                          ElevatorOrders.elevator_order_request_status == 1,
                          ElevatorOrders.elevator_order_demand_floor == update_info.current_floor,
                          ElevatorOrders.elevator_order_id == update_info.request_id,
                          ElevatorOrders.elevator_order_demand_category == 1) \
                  .update({'elevator_order_request_status': 2})

        db_session.commit()
    except Exception as error:
        db_session.rollback()
        raise DatabaseError(message="There was an unexpected error while updating the database",
                            original_exception=error)


##########################
# Delete current demand #
##########################

def delete_demand(delete_info: ElevatorDelete,
                  db_session: Session):
    try:
        delete_query = db_session.query(ElevatorOrders) \
                                 .filter(ElevatorOrders.elevator_id == delete_info.elevator_id,
                                         ElevatorOrders.elevator_order_request_status == 1,
                                         ElevatorOrders.elevator_order_id == delete_info.request_id)
        delete_query.first()
        delete_query.delete()
        db_session.commit()
    except Exception as error:
        db_session.rollback()
        raise DatabaseError(message="There was an unexpected error while deleting the database",
                            original_exception=error)
