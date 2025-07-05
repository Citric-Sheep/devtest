from fastapi.testclient import TestClient
from src.models import Demand
from unittest.mock import patch, MagicMock

from app import app

client = TestClient(app)

@patch('src.mongo.collection')
def test_call_elevator_success(mock_collection : MagicMock):
    '''
    Happy Request :)
    '''
    mock_collection.insert_one.return_value = MagicMock(inserted_id="mock_id_123")
    request_payload = {'src_floor' : -1, 'dest_floor' : 8, 'weight' : 75}
    response = client.post('/call', json=request_payload)
    assert response.status_code == 200
    assert response.json() == {'message' : 'OK'}

def test_call_elevator_invalid_floor():
    '''
    Business Logic Reproval
    '''
    request_payload = {"src_floor": 1, "dest_floor": 99, "weight": 75}
    response = client.post("/call", json=request_payload)
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_call_elevator_invalid_floors():
    '''
    Both src and dst floor are invalid and equal
    '''
    request_payload = {"src_floor": -99, "dest_floor": -99, "weight": 75}
    response = client.post("/call", json=request_payload)
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_same_floors():
    '''
    Same valid floors
    '''
    request_payload = {"src_floor": 10, "dest_floor": 10, "weight": 75}
    response = client.post("/call", json=request_payload)
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_call_overweight():
    '''
    Weight Logic Reproval
    '''
    request_payload = {"src_floor": 0, "dest_floor": 10, "weight": 900.1}
    response = client.post("/call", json=request_payload)
    
    assert response.status_code == 400
    assert "error" in response.json()

@patch('src.mongo.collection')
def test_get_formated_data_when_empty(mock_collection: MagicMock):
    mock_collection.find.return_value = []
    response = client.get("/formated_data")

    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'