import pytest
import json
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            # Drop all tables and recreate them
            db.drop_all()
            db.create_all()

            # Reset elevator to initial state
            from main import elevator
            elevator.reset()
            yield client


def test_call_elevator(client):
    """Test calling the elevator"""
    response = client.post('/call', json={'floor': 5, 'destination_floor': 10})
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Call received'
    assert data['call_floor'] == 5
    assert data['destination_floor'] == 10


def test_call_elevator_missing_floor(client):
    """Test calling elevator without floor"""
    response = client.post('/call', json={})
    assert response.status_code == 400


def test_step_simulation(client):
    """Test stepping the simulation"""
    # First call the elevator
    client.post('/call', json={'floor': 5})
    
    # Then step the simulation
    response = client.post('/step')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['message'] == 'Simulation stepped'
    assert data['moved'] == True


def test_get_status(client):
    """Test getting elevator status"""
    response = client.get('/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'elevator' in data
    assert 'total_logs' in data
    assert data['total_logs'] == 0  # No logs yet


def test_golden_event_logging(client):
    """Test that the golden event is logged when elevator is resting"""
    # Elevator starts resting
    response = client.get('/status')
    data = json.loads(response.data)
    assert data['elevator']['is_resting'] == True
    
    # Call the elevator
    client.post('/call', json={'floor': 5, 'destination_floor': 10})
    
    # Check that a log entry was created
    response = client.get('/logs')
    data = json.loads(response.data)
    assert len(data['logs']) == 1
    
    log = data['logs'][0]
    assert log['resting_floor'] == 1  # Started at floor 1
    assert log['call_floor'] == 5
    assert log['destination_floor'] == 10
    assert log['day_of_week'] >= 0 and log['day_of_week'] <= 6
    assert log['hour_of_day'] >= 0 and log['hour_of_day'] <= 23


def test_no_logging_when_not_resting(client):
    """Test that no log is created when elevator is not resting"""
    # Call elevator (this will log the first call)
    client.post('/call', json={'floor': 5})
    
    # Step only 2 times - elevator is still moving (at floor 3)
    for _ in range(2):
        client.post('/step')
    
    # Call again while elevator is actually moving (not resting)
    client.post('/call', json={'floor': 3})
    
    # Check logs - should only have 1 entry (the first call)
    response = client.get('/logs')
    data = json.loads(response.data)
    assert len(data['logs']) == 1

    # Verify the logs
    logs = data['logs']
    assert logs[0]['call_floor'] == 5  # First call


def test_no_logging_during_movement(client):
    """Test that no log is created when elevator is actively moving"""
    # Call elevator (this will log the first call)
    client.post('/call', json={'floor': 5})
    
    # Step once - elevator is moving (at floor 2)
    client.post('/step')
    
    # Verify elevator is not resting
    response = client.get('/status')
    data = json.loads(response.data)
    assert data['elevator']['is_resting'] == False
    
    # Call again while elevator is definitely moving
    client.post('/call', json={'floor': 3})
    
    # Check logs - should only have 1 entry (the first call)
    response = client.get('/logs')
    data = json.loads(response.data)
    assert len(data['logs']) == 1


def test_complete_elevator_cycle(client):
    """Test a complete elevator cycle with logging"""
    # 1. Elevator is resting at floor 1
    response = client.get('/status')
    data = json.loads(response.data)
    assert data['elevator']['is_resting'] == True
    assert data['elevator']['current_floor'] == 1
    
    # 2. Call from floor 5 to floor 10
    client.post('/call', json={'floor': 5, 'destination_floor': 10})
    
    # 3. Step until elevator reaches floor 5
    for i in range(4):
        response = client.post('/step')
        data = json.loads(response.data)
        print(f"Step {i+1}: moved={data['moved']}, floor={data['elevator_state']['current_floor']}")
        assert data['moved'] == True
    
    # 4. Arrive at floor 5 (should stop)
    response = client.post('/step')
    data = json.loads(response.data)
    print(f"Pick up passengers: moved={data['moved']}, floor={data['elevator_state']['current_floor']}")
    assert data['moved'] == False  # Stopped at floor 5 to pick up passengers

    # 5. Step until elevator reaches floor 10
    for i in range(5):
        response = client.post('/step')
        data = json.loads(response.data)
        print(f"Step {i+5}: moved={data['moved']}, floor={data['elevator_state']['current_floor']}")
        assert data['moved'] == True
    
    # 6. Arrive at floor 10 and start resting
    response = client.post('/step')
    data = json.loads(response.data)
    print(f"Final step: moved={data['moved']}, floor={data['elevator_state']['current_floor']}")
    assert data['moved'] == False  # No more destinations. Stopped and resting
    
    # 7. Check that elevator is resting again
    response = client.get('/status')
    data = json.loads(response.data)
    assert data['elevator']['is_resting'] == True
    assert data['elevator']['current_floor'] == 10
    
    # 8. Check that we have one log entry
    response = client.get('/logs')
    data = json.loads(response.data)
    assert len(data['logs']) == 1


def test_get_stats(client):
    """Test getting statistics"""
    # Create some test data
    client.post('/call', json={'floor': 5, 'destination_floor': 10})
    client.post('/step')  # Move to floor 2
    client.post('/step')  # Move to floor 3
    client.post('/step')  # Move to floor 4
    client.post('/step')  # Move to floor 5
    client.post('/step')  # Move to floor 6
    client.post('/step')  # Move to floor 7
    client.post('/step')  # Move to floor 8
    client.post('/step')  # Move to floor 9
    client.post('/step')  # Move to floor 10
    client.post('/step')  # Arrive and start resting
    
    # Now call from floor 3
    client.post('/call', json={'floor': 3, 'destination_floor': 7})
    
    response = client.get('/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'resting_patterns' in data
    assert len(data['resting_patterns']) > 0


def test_ml_training_data_generation(client):
    """Test that the system generates proper ML training data"""
    # Simulate multiple elevator cycles to generate training data
    floors = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Morning pattern: many calls from floor 1
    for i in range(5):
        # Ensure elevator is resting before calling
        response = client.get('/status')
        data = json.loads(response.data)
        if not data['elevator']['is_resting']:
            # Wait for elevator to finish current journey
            while not data['elevator']['is_resting']:
                client.post('/step')
                response = client.get('/status')
                data = json.loads(response.data)

        # Call from floor 1 to various floors
        client.post('/call', json={'floor': 1, 'destination_floor': floors[i % len(floors)]})
        
        # Move elevator to destination
        for _ in range(floors[i % len(floors)] - 1):
            client.post('/step')
        client.post('/step')  # Arrive and rest
    
    # Afternoon pattern: calls from middle floors
    for i in range(3):
        # Ensure elevator is resting before calling
        response = client.get('/status')
        data = json.loads(response.data)
        if not data['elevator']['is_resting']:
            # Wait for elevator to finish current journey
            while not data['elevator']['is_resting']:
                client.post('/step')
                response = client.get('/status')
                data = json.loads(response.data)

        call_floor = floors[2 + (i % 6)]  # Floors 3-8
        client.post('/call', json={'floor': call_floor, 'destination_floor': 1})
        
        # Move elevator to destination
        for _ in range(abs(call_floor - 1)):
            client.post('/step')
        client.post('/step')  # Arrive and rest
    
    # Get logs for ML training
    response = client.get('/logs')
    data = json.loads(response.data)
    
    # Verify we have meaningful training data
    assert len(data['logs']) == 8  # 5 morning + 3 afternoon calls
    
    # Check that floor 1 has the most calls (morning rush)
    floor_1_calls = sum(1 for log in data['logs'] if log['call_floor'] == 1)
    assert floor_1_calls >= 5  # At least 5 calls from floor 1
    
    # Verify all logs have proper ML features
    for log in data['logs']:
        assert 'resting_floor' in log
        assert 'call_floor' in log
        assert 'day_of_week' in log
        assert 'hour_of_day' in log
        assert 'idle_time_seconds' in log
        assert log['idle_time_seconds'] > 0


if __name__ == '__main__':
    pytest.main([__file__]) 