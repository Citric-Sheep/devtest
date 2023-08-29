##############
# Libraries #
##############

import logging

from pathlib import Path
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.db_utilities import db_connection

from apps.elevator.elevator_schemas import ElevatorDemand, ElevatorUpdate
from apps.elevator.elevator_crud import add_demand, check_demand, update_demands

##########################
# Router main directory #
##########################

main_directory = Path(__file__).resolve().parent.parent

#########################
# Logger Configuration #
#########################

logger = logging.getLogger(__name__)

#####################
# Router execution #
#####################

elevator_router = APIRouter(tags=['Elevator'])

##############
# Elevator  #
##############


@elevator_router.post('/elevator/demand')
async def elevator_demand(demand_request: ElevatorDemand,
                          db: Session = Depends(db_connection)):
    logger.info("Attempting to process user demand")
    add_demand(demand_request, db)
    current_demand = check_demand(demand_request, db)
    logger.info("User demand processed successfully")
    return current_demand


@elevator_router.put('/elevator/demand')
async def elevator_update(update_data: ElevatorUpdate,
                          db: Session = Depends(db_connection)):
    logger.info("Attempting to update elevator demands")
    update_demands(update_data, db)
    demand_data = ElevatorDemand(elevator_id=update_data.elevator_id,
                                 current_floor=update_data.current_floor,
                                 destination_floor=update_data.current_floor,
                                 current_movement=update_data.current_movement,
                                 demand_category=-1,
                                 demand_type=-1)
    current_demand = check_demand(demand_data, db)
    logger.info("Demands successfully updated")
    return current_demand
