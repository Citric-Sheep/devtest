from flask import Flask
from db import elevator
from routes.elevator_routes import elevator_api_routes
from routes.elevator_records_ml import elevator_records_ml


def create_app():
    flask_app = Flask(__name__)

    elevator.create_database()
    elevator.create_elevator_tables()

    flask_app.register_blueprint(elevator_api_routes)
    flask_app.register_blueprint(elevator_records_ml)

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
