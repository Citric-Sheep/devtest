from fastapi import FastAPI
from app.api.v1.endpoints import routes_demand, routes_resting

app = FastAPI()

app.include_router(routes_demand.router)
app.include_router(routes_resting.router)
