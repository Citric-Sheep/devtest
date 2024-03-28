import pytest
from server import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.order(6)
def test_create_demand(client):
    # Test case for creating a new demand
    data = {
        "custom_id": 2,
        "elevator_id": 2,
        "start_floor": 2,
        "end_floor": 3
    }
    response = client.post('/demand/create', json=data)
    assert response.status_code == 201


@pytest.mark.order(12)
def test_get_demands(client):
    response = client.get('/demand/get')
    assert response.status_code == 200


@pytest.mark.order(18)
def test_get_demands_with_elevator_id(client):
    response = client.get('/demand/get/2')
    assert response.status_code == 200


@pytest.mark.order(21)
def test_update_demand(client):
    data = {
        "id": 1,
        "new_values": {
            "end_floor": 4
        }
    }
    response = client.put('/demand/update', json=data)
    assert response.status_code == 200


@pytest.mark.order(20)
def test_delete_demand(client):
    data = {
        "id": 2
    }
    response = client.delete('/demand/delete', json=data)
    assert response.status_code == 200
