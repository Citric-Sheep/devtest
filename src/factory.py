from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI

from .routers import demand_router
from .routers import elevator_router
from .routers import floor_router

from .config import settings

from datetime import datetime
import pytz

import logging
logger = logging.getLogger()


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def converter(self, timestamp):
        dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        return dt.astimezone(pytz.timezone(settings.TZ))

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s

def config_logging(debug=False):

    logger = logging.getLogger()

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d/%m/%Y %H:%M:%S")

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # Adicionando o handlers
    logger.addHandler(ch)

def create_app(debug: bool = False) -> FastAPI:
    
    app = FastAPI()
    app.debug = debug
    config_logging(debug)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(demand_router.router)
    app.include_router(elevator_router.router)
    app.include_router(floor_router.router)

    return app