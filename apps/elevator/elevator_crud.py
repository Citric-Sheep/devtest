##############
# Libraries #
##############

from sqlalchemy import asc
from sqlalchemy.orm import Session

from database.db_models import ElevatorOrders

from apps.elevator.elevator_schemas import ElevatorDemand, ElevatorUpdate
from apps.elevator.elevator_utilities import Elevator


##################################################
# Add data to the log and see requests in order #
##################################################

def add_demand(demand_info: ElevatorDemand,
               db_session: Session):
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


def check_demand(demand_info: ElevatorDemand,
                 db_session: Session):
    records = db_session.query(ElevatorOrders).filter(ElevatorOrders.elevator_id == demand_info.elevator_id,
                                                      ElevatorOrders.elevator_order_request_status == 1)\
                        .order_by(asc(ElevatorOrders.elevator_order_update_on)).all()

    elevator = Elevator(records, demand_info.current_movement, demand_info.current_floor)
    elevator_demand = elevator.target_floor()
    return elevator_demand


def update_demands(update_info: ElevatorUpdate,
                   db_session: Session):
    if update_info.current_movement in [1, 2]:
        demand_type = update_info.current_movement
    else:
        demand_type = None

    db_session.query(ElevatorOrders) \
              .filter(ElevatorOrders.elevator_id == update_info.elevator_id,
                      ElevatorOrders.elevator_order_request_status == 1,
                      ElevatorOrders.elevator_order_demand_floor == update_info.current_floor,
                      ElevatorOrders.elevator_order_demand_category == 2) \
              .update({'elevator_order_request_status': 2})
    if demand_type:
        db_session.query(ElevatorOrders) \
                  .filter(ElevatorOrders.elevator_id == update_info.elevator_id,
                          ElevatorOrders.elevator_order_request_status == 1,
                          ElevatorOrders.elevator_order_demand_floor == update_info.current_floor,
                          ElevatorOrders.elevator_order_demand_type == demand_type,
                          ElevatorOrders.elevator_order_demand_category == 1) \
                  .update({'elevator_order_request_status': 2})

    db_session.commit()
