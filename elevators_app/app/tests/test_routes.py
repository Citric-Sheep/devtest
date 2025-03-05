import pytest
from app import create_app
from app.models import Elevator, Demand
from app.database import db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_create_demand(client):
    response = client.post('/call_elevator', json={
        'floor': 5,
        'elevator_id': 1
    })
    assert response.status_code == 201
    assert Demand.query.count() == 1

def test_update_elevator(client):
    elevator = Elevator(current_floor=1, status='idle', resting_floor=1)
    db.session.add(elevator)
    db.session.commit()

    response = client.post('/elevator/update', json={
        'elevator_id': 1,
        'current_floor': 3,
        'status': 'idle'
    })
    assert response.status_code == 200
    assert Elevator.query.get(1).current_floor == 3

def test_create_elevator(client):
    response = client.post('/elevator')
    assert response.status_code == 201
    assert Elevator.query.count() == 1