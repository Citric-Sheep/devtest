# -*- coding: utf-8 -*-
import pytest
from datetime import datetime,timedelta
from app import app,db
from app.models import ElevatorState

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client


def test_create_demand(client):
    response = client.post('/demand',json={"actual_floor":3,"target_floor":6})
    assert response.status_code == 201
    assert response.json == {"message":"Demand created"}

def test_create_state(client):
    response = client.post('/state',json={"floor":2,"vacant":True})
    assert response.status_code == 201
    assert response.json == {"message":"State created"}
    
def test_relocation(client):
    response = client.post('/state',json={"floor":2,"vacant":True})
    state_id = 1
    end_time = datetime.utcnow() + timedelta(seconds=100)
    response = client.patch(f'/state/{state_id}/end',json={"end_time":f"{end_time.isoformat()}"})
    assert response.status_code == 201
    assert response.json == {"message":"State changed"}
    state = ElevatorState.query.filter_by(id=state_id).first()
    assert not state.relocation_flag
    
def test_idle_relocation(client):
    response = client.post('/state',json={"floor":2,"vacant":True})
    state_id = 1
    end_time = datetime.utcnow() + timedelta(seconds=600)
    response = client.patch(f'/state/{state_id}/end',json={"end_time":f"{end_time.isoformat()}"})
    assert response.status_code == 201
    assert response.json == {"message":"State changed"}
    state = ElevatorState.query.filter_by(id=state_id).first()
    assert state.relocation_flag


