##############
# Libraries #
##############

import logging

from fastapi import FastAPI

from configuration.configuration import configure_project_attributes

from apps.elevator import elevator_router

#########################
# Logger Configuration #
#########################

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

######################
# APP Configuration #
######################

app_main = FastAPI(title=configure_project_attributes.PROJECT_NAME,
                   version=configure_project_attributes.PROJECT_VERSION)

#####################
# APP main routers #
#####################

app_main.include_router(elevator_router.elevator_router)
