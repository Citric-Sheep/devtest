##############
# Libraries #
##############

import logging
import traceback

from pathlib import Path
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.db_utilities import db_connection

from apps.elevator.elevator_schemas import ElevatorCheck, ElevatorDemand, ElevatorUpdate, ElevatorStatus, ElevatorDelete
from apps.elevator.elevator_crud import add_demand, check_demand, update_demands, delete_demand, add_status
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
        check_data = ElevatorCheck(elevator_id=demand_data.elevator_id,
                                   current_floor=demand_data.current_floor,
                                   current_movement=demand_data.current_movement)
        current_demand = check_demand(demand_info=check_data,
                                      db_session=db)
        logger.info("User demand processed successfully")
        return current_demand
    except DatabaseError as error:
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
        check_data = ElevatorCheck(elevator_id=update_data.elevator_id,
                                   current_floor=update_data.current_floor,
                                   current_movement=update_data.current_movement)
        current_demand = check_demand(demand_info=check_data,
                                      db_session=db)
        logger.info("Demands successfully updated")
        return current_demand
    except DatabaseError as error:
        traceback.print_exc()
        logger.error("There was a database error while processing the user request: {error_exception}".format(error_exception=error.original_exception))
        raise error
    except Exception as error:
        logger.error("There was an unexpected error while processing the user request: {error_exception}".format(error_exception=error))
        raise ServerError(message="There was an unexpected error while processing the user request",
                          original_exception=error)


@elevator_router.delete('/elevator/demand')
async def elevator_delete(delete_data: ElevatorDelete,
                          db: Session = Depends(db_connection)):
    try:
        logger.info("Attempting to delete elevator demand")
        delete_demand(delete_info=delete_data,
                      db_session=db)
        check_data = ElevatorCheck(elevator_id=delete_data.elevator_id,
                                   current_floor=delete_data.current_floor,
                                   current_movement=delete_data.current_movement)
        current_demand = check_demand(demand_info=check_data,
                                      db_session=db)
        logger.info("Elevator demand deleted successfully")
        return current_demand
    except DatabaseError as error:
        logger.error("There was a database error while processing the user request: {error_exception}".format(error_exception=error.original_exception))
        raise error
    except Exception as error:
        logger.error("There was an unexpected error while processing the user request: {error_exception}".format(error_exception=error))
        raise ServerError(message="There was an unexpected error while processing the user request",
                          original_exception=error)


@elevator_router.post('/elevator/status')
async def elevator_status(demand_data: ElevatorStatus,
                          db: Session = Depends(db_connection)):
    try:
        logger.info("Attempting to add elevator status")
        add_status(status_info=demand_data,
                   db_session=db)
        logger.info("Elevator status added successfully")
    except DatabaseError as error:
        logger.error("There was a database error while processing the user request: {error_exception}".format(error_exception=error.original_exception))
        raise error
    except Exception as error:
        logger.error("There was an unexpected error while processing the user request: {error_exception}".format(error_exception=error))
        raise ServerError(message="There was an unexpected error while processing the user request",
                          original_exception=error)
