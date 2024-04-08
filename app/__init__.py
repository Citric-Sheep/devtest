""" FastAPI implementation """

from fastapi import FastAPI

from app.config.database import create_database
from app.constants import DOCS_TITLE
from app.routers import default_router, demand_router

app = FastAPI(debug=True, title=DOCS_TITLE, docs_url="/docs")

create_database()

app.include_router(router=default_router)
app.include_router(router=demand_router)
