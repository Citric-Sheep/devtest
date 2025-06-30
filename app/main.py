import logging
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database.elevators import Base, engine
from app.routers.elevators import router as main_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Prediction_Engine")


@app.on_event("startup")
def on_startup():
    """
    Function executed once when the FastAPI app starts.
    It ensures that all database tables defined in the SQLAlchemy models are created.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("SQLite schema ready")


app.include_router(main_router)
