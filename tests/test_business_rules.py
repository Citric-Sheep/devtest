import json
import pytest
from datetime import datetime, timedelta
from src.models import ElevatorCall, ElevatorTrip, ElevatorState, TimeStatistic, FloorStatistic

class TestElevatorBehavior:
    def test_elevator_call_updates_statistics(self, client, sample_elevator, db_session):
        # Create a call
        response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        assert response.status_code == 201
        
        # Check time statistics
        today = datetime.now().date()
        current_hour = datetime.now().hour
        
        time_stat = db_session.query(TimeStatistic).filter(
            TimeStatistic.elevator_id == sample_elevator.id,
            TimeStatistic.date == today,
            TimeStatistic.hour == current_hour
        ).first()
        
        assert time_stat is not None
        assert time_stat.calls_count == 1
        
        # Check floor statistics
        floor_stat = db_session.query(FloorStatistic).filter(
            FloorStatistic.elevator_id == sample_elevator.id,
            FloorStatistic.floor == 3,
            FloorStatistic.date == today
        ).first()
        
        assert floor_stat is not None
        assert floor_stat.calls_count == 1
        
        # Create another call from the same floor
        response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'down'
        })
        
        assert response.status_code == 201
        
        # Check statistics are updated
        db_session.refresh(time_stat)
        db_session.refresh(floor_stat)
        
        assert time_stat.calls_count == 2
        assert floor_stat.calls_count == 2
    
    def test_trip_completion_updates_wait_time(self, client, sample_elevator, db_session):
        # Create a call
        call_response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        assert call_response.status_code == 201
        
        # Create a trip to respond to the call (elevator moving to the call floor)
        trip_response = client.post(f'/elevators/{sample_elevator.id}/trips', json={
            'origin_floor': 1,
            'destination_floor': 3,
            'occupancy': False  # Empty elevator going to pick up
        })
        
        assert trip_response.status_code == 201
        trip_id = json.loads(trip_response.data)['id']
        
        # Complete the trip
        complete_response = client.post(f'/elevators/{sample_elevator.id}/trips/{trip_id}/complete')
        assert complete_response.status_code == 200
        
        # Check that the call's wait time was updated
        call = db_session.query(ElevatorCall).filter(
            ElevatorCall.elevator_id == sample_elevator.id,
            ElevatorCall.floor == 3
        ).order_by(ElevatorCall.timestamp.desc()).first()
        
        assert call is not None
        assert call.wait_time is not None
        assert call.wait_time > 0
        
        # Check that floor statistics were updated with wait time
        today = datetime.now().date()
        floor_stat = db_session.query(FloorStatistic).filter(
            FloorStatistic.elevator_id == sample_elevator.id,
            FloorStatistic.floor == 3,
            FloorStatistic.date == today
        ).first()
        
        assert floor_stat is not None
        assert floor_stat.avg_wait_time is not None
        assert floor_stat.avg_wait_time > 0
    
    def test_elevator_state_tracking(self, client, sample_elevator, db_session):
        # Create initial state
        state_response = client.post(f'/elevators/{sample_elevator.id}/states', json={
            'floor': 1,
            'is_vacant': True,
            'is_moving': False
        })
        
        assert state_response.status_code == 201
        
        # Create a call
        call_response = client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 5,
            'direction': 'down'
        })
        
        assert call_response.status_code == 201
        
        # Create a trip (elevator moving to the call floor)
        trip_response = client.post(f'/elevators/{sample_elevator.id}/trips', json={
            'origin_floor': 1,
            'destination_floor': 5,
            'occupancy': False
        })
        
        assert trip_response.status_code == 201
        trip_id = json.loads(trip_response.data)['id']
        
        # Check that elevator state was updated to moving
        current_state_response = client.get(f'/elevators/{sample_elevator.id}/states/current')
        assert current_state_response.status_code == 200
        current_state = json.loads(current_state_response.data)
        
        assert current_state['is_moving'] is True
        assert current_state['is_vacant'] is True
        assert current_state['is_resting'] is False
        
        # Complete the trip
        complete_response = client.post(f'/elevators/{sample_elevator.id}/trips/{trip_id}/complete')
        assert complete_response.status_code == 200
        
        # Check that elevator state was updated to stationary at the destination floor
        current_state_response = client.get(f'/elevators/{sample_elevator.id}/states/current')
        assert current_state_response.status_code == 200
        current_state = json.loads(current_state_response.data)
        
        assert current_state['is_moving'] is False
        assert current_state['is_vacant'] is True
        assert current_state['is_resting'] is True
        assert current_state['floor'] == 5
    
    def test_optimal_resting_floor_calculation(self, client, sample_elevator, db_session):
        # Create multiple calls from different floors to establish a pattern
        for _ in range(3):
            client.post(f'/elevators/{sample_elevator.id}/calls', json={
                'floor': 3,
                'direction': 'up'
            })
        
        for _ in range(2):
            client.post(f'/elevators/{sample_elevator.id}/calls', json={
                'floor': 7,
                'direction': 'down'
            })
        
        # Get the optimal resting floor
        response = client.get(f'/ml/optimal_resting_floor?elevator_id={sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # The optimal floor should be the one with the most calls (floor 3)
        assert data['optimal_resting_floor'] == 3
        
        # Add more calls from floor 7 to change the optimal floor
        for _ in range(4):
            client.post(f'/elevators/{sample_elevator.id}/calls', json={
                'floor': 7,
                'direction': 'down'
            })
        
        # Get the optimal resting floor again
        response = client.get(f'/ml/optimal_resting_floor?elevator_id={sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # The optimal floor should now be floor 7
        assert data['optimal_resting_floor'] == 7

class TestMLDataPreparation:
    def test_time_based_statistics(self, client, sample_elevator, db_session):
        # Create calls at different hours by manipulating the timestamp
        current_time = datetime.now()
        
        # Create a call for the current hour
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        # Manually insert calls for a different hour
        different_hour = (current_time.hour + 1) % 24
        different_hour_call = ElevatorCall(
            elevator_id=sample_elevator.id,
            floor=5,
            direction='down',
            timestamp=current_time.replace(hour=different_hour)
        )
        db_session.add(different_hour_call)
        
        # Manually create time statistics for the different hour
        different_hour_stat = TimeStatistic(
            elevator_id=sample_elevator.id,
            date=current_time.date(),
            hour=different_hour,
            calls_count=1,
            most_common_origin_floor=5
        )
        db_session.add(different_hour_stat)
        db_session.commit()
        
        # Get time statistics
        response = client.get(f'/ml/time_statistics?elevator_id={sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should have statistics for both hours
        assert len(data) >= 2
        
        # Check that we have stats for both hours
        hours = [stat['hour'] for stat in data]
        assert current_time.hour in hours
        assert different_hour in hours
    
    def test_floor_based_statistics(self, client, sample_elevator, db_session):
        # Create calls from different floors
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 3,
            'direction': 'up'
        })
        
        client.post(f'/elevators/{sample_elevator.id}/calls', json={
            'floor': 7,
            'direction': 'down'
        })
        
        # Get floor statistics
        response = client.get(f'/ml/floor_statistics?elevator_id={sample_elevator.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should have statistics for both floors
        assert len(data) >= 2
        
        # Check that we have stats for both floors
        floors = [stat['floor'] for stat in data]
        assert 3 in floors
        assert 7 in floors
        
        # Check call counts
        floor_3_stat = next(stat for stat in data if stat['floor'] == 3)
        floor_7_stat = next(stat for stat in data if stat['floor'] == 7)
        
        assert floor_3_stat['calls_count'] >= 1
        assert floor_7_stat['calls_count'] >= 1