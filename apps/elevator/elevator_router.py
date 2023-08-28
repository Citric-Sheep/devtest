##############
# Libraries #
##############

import logging

from pathlib import Path
from fastapi import APIRouter

from apps.elevator.elevator_schemas import ElevatorDemand

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
async def elevator_demand(demand_info: ElevatorDemand):
    return demand_info


@elevator_router.put('/elevator/demand')
async def elevator_update():
    return {'message': 'Elevator demand updated'}
