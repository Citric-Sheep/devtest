from flask import Flask
from .building_endpoints import building_blueprint
from .elevator_endpoints import elevator_blueprint
from .demand_endpoints import demand_blueprint
from utils.db import PostgreSQLHandler


# DB initialized here

psql = PostgreSQLHandler()
psql.init_db()

# Here we create the flask app.
app = Flask(__name__)

# Blueprints are registered.
app.register_blueprint(building_blueprint, url_prefix="/building")
app.register_blueprint(elevator_blueprint, url_prefix="/elevator")
app.register_blueprint(demand_blueprint, url_prefix="/demand")