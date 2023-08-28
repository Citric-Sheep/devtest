##############
# Libraries #
##############

import logging

from pathlib import Path
from fastapi import APIRouter

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
async def elevator_demand():
    return {'Hola mundo :D': 'Chao Mundo D:'}
