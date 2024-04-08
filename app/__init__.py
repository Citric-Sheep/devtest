""" FastAPI implementation """

from fastapi import FastAPI

from app.config.database import create_database
from app.routers import default_router, demand_router

app = FastAPI(debug=True, title="Elevator Demand Records")


@app.on_event("startup")
def on_startup() -> None:
    """To execute when app is started."""
    create_database()


app.include_router(router=default_router)
app.include_router(router=demand_router)
