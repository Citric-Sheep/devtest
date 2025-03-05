import pytest
from app import create_app
from app.models import Elevator, Demand, ElevatorHistory
from app.database import db



@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_elevator_model(app):
    elevator = Elevator(current_floor=1, status='resting', resting_floor=1)
    db.session.add(elevator)
    db.session.commit()
    assert Elevator.query.count() == 1


def test_demand_model(app):
    demand = Demand(floor_number=5)
    db.session.add(demand)
    db.session.commit()
    assert Demand.query.count() == 1