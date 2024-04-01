from flask import Flask
from db import elevator
from routes.elevator_routes import elevator_routes, elevator_api_routes

from routes import init_routes


def create_app():
    flask_app = Flask(__name__)

    elevator.create_database()
    elevator.create_elevator_tables()

    flask_app.register_blueprint(init_routes)
    flask_app.register_blueprint(elevator_routes)
    flask_app.register_blueprint(elevator_api_routes)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
