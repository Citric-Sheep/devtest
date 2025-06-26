import pytest
from main import app, db


# Set up test client with in-memory SQLite database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


# Tests elevator_demands
def test_create_demand(client):
    # Test creating a demand with a valid floor and dynamic timestamp
    response = client.post('/demand', json={'floor': 3})
    response_data = response.get_json()
    demand_data = response_data['demand']
    actual_id = demand_data['id']
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Demand created', 'demand': {
        'id': actual_id,
        'timestamp': response.get_json()['demand']['timestamp'],  # Handle dynamic timestamp
        'floor': 3,
        'day_of_week': response.get_json()['demand']['day_of_week'],
        'hour_of_day': response.get_json()['demand']['hour_of_day']
    }}


def test_create_demand_invalid_floor(client):
    # Check that we get a 400 error if floor isn't an integer
    response = client.post('/demand', json={'floor': 'hola'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Floor must be an integer'}


def test_get_demand(client):
    client.post('/demand', json={'floor': 1})
    response = client.get('/demand/1')
    assert response.status_code == 200
    assert response.get_json()['floor'] == 1


def test_get_demand_not_found(client):
    # Test that requesting a non-existent demand returns 404
    response = client.get('/demand/hola')
    assert response.status_code == 404


def test_get_all_demands(client):
    client.post('/demand', json={'floor': 3})
    client.post('/demand', json={'floor': -1})
    response = client.get('/demands')
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_update_demand(client):
    client.post('/demand', json={'floor': 1})
    response = client.put('/demand/1', json={'floor': 50})
    assert response.status_code == 200
    assert response.get_json()['demand']['floor'] == 50


def test_update_demand_invalid_floor(client):
    # Test that updating with an invalid floor gives a 400 error
    client.post('/demand', json={'floor': 1})
    response = client.put('/demand/1', json={'floor': 'invalid'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Floor must be an integer'}


def test_delete_demand(client):
    client.post('/demand', json={'floor': -5})
    response = client.delete('/demand/1')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Demand deleted'}
    response = client.get('/demand/1')
    assert response.status_code == 404


# Test elevator_states
def test_create_state(client):
    client.post('/demand', json={'floor': -3})  # Set up a demand for other test
    response = client.post('/state', json={'floor': 5, 'vacant': True})
    assert response.status_code == 201
    assert response.get_json()['state']['floor'] == 5
    assert response.get_json()['state']['vacant'] is True


def test_create_state_non_vacant_valid_demand(client):
    # Test creating a non-vacant state with a valid demand_id
    client.post('/demand', json={'floor': 3})
    response = client.post('/state', json={'floor': 3, 'vacant': False, 'demand_id': 1})
    assert response.status_code == 201
    assert response.get_json()['state']['demand_id'] == 1


def test_create_state_non_vacant_invalid_demand(client):
    # Check that a non-vacant state with an invalid demand_id fails
    response = client.post('/state', json={'floor': 3, 'vacant': False, 'demand_id': 999})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid demand_id'}


def test_create_state_non_vacant_no_demand_id(client):
    # Test that a non-vacant state without demand_id returns an error
    response = client.post('/state', json={'floor': 3, 'vacant': False})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Non-vacant state requires a valid demand_id'}


def test_create_state_invalid_floor(client):
    # Test that an invalid floor in state creation gives a 400 error
    response = client.post('/state', json={'floor': 'invalid', 'vacant': True})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Floor must be an integer'}


def test_create_state_invalid_vacant(client):
    # Check that an invalid vacant value fails with a 400
    response = client.post('/state', json={'floor': 5, 'vacant': 'invalid'})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Vacant must be a boolean'}


def test_get_state(client):
    # Test read to obtain a 200
    client.post('/demand', json={'floor': 3})
    client.post('/state', json={'floor': 5, 'vacant': True})
    response = client.get('/state/1')
    assert response.status_code == 200
    assert response.get_json()['floor'] == 5


def test_get_state_not_found(client):
    # Test that requesting a non-existent state returns 404
    response = client.get('/state/999')
    assert response.status_code == 404


def test_get_all_states(client):
    # Test to obtain all the states and get a 200
    client.post('/demand', json={'floor': 3})
    client.post('/state', json={'floor': 5, 'vacant': True})
    client.post('/state', json={'floor': -1, 'vacant': False, 'demand_id': 1})
    response = client.get('/states')
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_update_state(client):
    # Test updtae to obtain a 200
    client.post('/demand', json={'floor': 3})
    client.post('/state', json={'floor': 5, 'vacant': True})
    response = client.put('/state/1', json={'floor': -1, 'vacant': False, 'demand_id': 1})
    assert response.status_code == 200
    assert response.get_json()['state']['floor'] == -1
    assert response.get_json()['state']['vacant'] is False


def test_update_state_invalid_demand_id(client):
    # Test updating a state with an invalid demand_id and obtain a 400
    client.post('/state', json={'floor': 5, 'vacant': True})
    response = client.put('/state/1', json={'floor': 5, 'vacant': False, 'demand_id': 999})
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Invalid demand_id'}


def test_delete_state(client):
    client.post('/state', json={'floor': 5, 'vacant': True})
    response = client.delete('/state/1')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'State deleted'}
    response = client.get('/state/1')
    assert response.status_code == 404