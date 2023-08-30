##############
# Libraries #
##############

import logging
import traceback

from pathlib import Path
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.db_utilities import db_connection

from apps.elevator.elevator_schemas import ElevatorDemand, ElevatorUpdate
from apps.elevator.elevator_crud import add_demand, check_demand, update_demands
from apps.elevator.elevator_exceptions import DatabaseError, ServerError

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
async def elevator_demand(demand_data: ElevatorDemand,
                          db: Session = Depends(db_connection)):
    try:
        logger.info("Attempting to process user demand")
        add_demand(demand_info=demand_data,
                   db_session=db)
        current_demand = check_demand(demand_info=demand_data,
                                      db_session=db)
        logger.info("User demand processed successfully")
        return current_demand
    except DatabaseError as error:
        traceback.print_exc()
        logger.error("There was a database error while processing the user request: {error_exception}".format(error_exception=error.original_exception))
        raise error
    except Exception as error:
        logger.error("There was an unexpected error while processing the user request: {error_exception}".format(error_exception=error))
        raise ServerError(message="There was an unexpected error while processing the user request",
                          original_exception=error)


@elevator_router.put('/elevator/demand')
async def elevator_update(update_data: ElevatorUpdate,
                          db: Session = Depends(db_connection)):
    try:
        logger.info("Attempting to update elevator demands")
        update_demands(update_info=update_data,
                       db_session=db)
        current_demand = check_demand(demand_info=update_data,
                                      db_session=db)
        logger.info("Demands successfully updated")
        return current_demand
    except DatabaseError as error:
        logger.error("There was a database error while processing the user request: {error_exception}".format(error_exception=error.original_exception))
        raise error
    except Exception as error:
        logger.error("There was an unexpected error while processing the user request: {error_exception}".format(error_exception=error))
        raise ServerError(message="There was an unexpected error while processing the user request",
                          original_exception=error)
