import json
import pytest
from datetime import datetime, date

class TestBuildingAPI:
    def test_create_building(self, client):
        response = client.post('/buildings', json={
            'name': 'Test Building',
            'floors': 10
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Building'
        assert data['floors'] == 10
        assert 'id' in data
        assert 'created_at' in data
    
    def test_get_buildings(self, client, sample_building):
        response = client.get('/buildings')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(b['id'] == sample_building.id for b in data)
    
    def test_get_building(self, client, sample_building):
        response = client.get(f'/buildings/{sample_building.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_building.id
        assert data['name'] == sample_building.name
        assert data['floors'] == sample_building.floors
    
    def test_get_nonexistent_building(self, client):
        response = client.get('/buildings/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Not found' in data['error']

class TestElevatorAPI:
    def test_create_elevator(self, client, sample_building):
        response = client.post(f'/buildings/{sample_building.id}/elevators', json={
            'name': 'Test Elevator'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Elevator'
        assert data['building_id'] == sample_building.id
        assert 'id' in data
        assert 'created_at' in data
    
    def test_get_elevators(self, client, sample_building, sample_elevator):
        response = client.get(f'/buildings/{sample_building.id}/elevators')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(e['id'] == sample_elevator.id for e in data)
    
    def test_get_elevator(self, client, sample_elevator):
        response = client.get(f'/elevators/{sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_elevator.id
        assert data['name'] == sample_elevator.name
        assert data['building_id'] == sample_elevator.building_id
    
    def test_get_nonexistent_elevator(self, client):
        response = client.get('/elevators/9999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Not found' in data['error']

class TestElevatorCallAPI:
    def test_create_call(self, client, sample_elevator, db_session):
        response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['floor'] == 3
        assert data['direction'] == 'up'
        assert data['elevator_id'] == sample_elevator.id
        assert 'id' in data
        assert 'timestamp' in data
    
    def test_create_call_invalid_direction(self, client, sample_elevator):
        response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'sideways'  # Invalid direction
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Bad request' in data['error']
    
    def test_get_calls(self, client, sample_elevator, db_session):
        # Create a call first
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        response = client.get(f'/elevators/{sample_elevator.id}/calls')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['floor'] == 3
        assert data[0]['direction'] == 'up'

class TestElevatorTripAPI:
    def test_create_trip(self, client, sample_elevator):
        response = client.post(f'/elevators/{sample_elevator.id}/trips', json={
            'origin_floor': 2,
            'destination_floor': 8,
            'occupancy': True
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['origin_floor'] == 2
        assert data['destination_floor'] == 8
        assert data['occupancy'] is True
        assert data['elevator_id'] == sample_elevator.id
        assert 'id' in data
        assert 'start_time' in data
    
    def test_complete_trip(self, client, sample_elevator, db_session):
        # Create a trip first
        response = client.post(f'/elevators/{sample_elevator.id}/trips', json={
            'origin_floor': 2,
            'destination_floor': 8,
            'occupancy': True
        })
        trip_id = json.loads(response.data)['id']
        
        # Complete the trip
        response = client.post(f'/elevators/{sample_elevator.id}/trips/{trip_id}/complete')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == trip_id
        assert data['origin_floor'] == 2
        assert data['destination_floor'] == 8
        assert data['occupancy'] is True
        assert 'end_time' in data
        assert 'duration' in data
    
    def test_get_trips(self, client, sample_elevator, db_session):
        # Create a trip first
        client.post(f'/elevators/{sample_elevator.id}/trips', json={
            'origin_floor': 2,
            'destination_floor': 8,
            'occupancy': True
        })
        
        response = client.get(f'/elevators/{sample_elevator.id}/trips')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['origin_floor'] == 2
        assert data[0]['destination_floor'] == 8

class TestElevatorStateAPI:
    def test_create_state(self, client, sample_elevator):
        response = client.post(f'/elevators/{sample_elevator.id}/states', json={
            'floor': 5,
            'is_vacant': True,
            'is_moving': False
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['floor'] == 5
        assert data['is_vacant'] is True
        assert data['is_moving'] is False
        assert data['is_resting'] is True
        assert data['elevator_id'] == sample_elevator.id
        assert 'id' in data
        assert 'timestamp' in data
    
    def test_get_states(self, client, sample_elevator, db_session):
        # Create a state first
        client.post(f'/elevators/{sample_elevator.id}/states', json={
            'floor': 5,
            'is_vacant': True,
            'is_moving': False
        })
        
        response = client.get(f'/elevators/{sample_elevator.id}/states')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['floor'] == 5
        assert data[0]['is_vacant'] is True
        assert data[0]['is_moving'] is False
    
    def test_get_current_state(self, client, sample_elevator, db_session):
        # Create a state first
        client.post(f'/elevators/{sample_elevator.id}/states', json={
            'floor': 5,
            'is_vacant': True,
            'is_moving': False
        })
        
        response = client.get(f'/elevators/{sample_elevator.id}/states/current')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['floor'] == 5
        assert data['is_vacant'] is True
        assert data['is_moving'] is False
        assert data['is_resting'] is True

class TestMLDataAPI:
    def test_get_time_statistics(self, client, sample_elevator, db_session):
        # No statistics yet
        response = client.get('/ml/time_statistics')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        
        # Create a call to generate statistics
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        # Check statistics with elevator_id filter
        response = client.get(f'/ml/time_statistics?elevator_id={sample_elevator.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['elevator_id'] == sample_elevator.id
        assert data[0]['calls_count'] >= 1
    
    def test_get_floor_statistics(self, client, sample_elevator, db_session):
        # No statistics yet
        response = client.get('/ml/floor_statistics')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        
        # Create a call to generate statistics
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        # Check statistics with elevator_id and floor filters
        response = client.get(f'/ml/floor_statistics?elevator_id={sample_elevator.id}&floor=3')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['elevator_id'] == sample_elevator.id
        assert data[0]['floor'] == 3
        assert data[0]['calls_count'] >= 1
    
    def test_get_optimal_resting_floor(self, client, sample_elevator, db_session):
        response = client.get(f'/ml/optimal_resting_floor?elevator_id={sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['elevator_id'] == sample_elevator.id
        assert 'optimal_resting_floor' in data
        assert 'timestamp' in data