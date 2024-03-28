import pytest
from server import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.order(2)
def test_create_building(client):
    # Test case for creating a new building
    data = {
        "custom_id": 2,
        "name": "Test Building",
        "address": "123 Main St",
        "city": "Test City",
        "country": "Test Country"
    }
    response = client.post('/building/create', json=data)
    assert response.status_code == 201


@pytest.mark.order(8)
def test_get_building(client):
    response = client.get('/building/get')
    assert response.status_code == 200
    assert len(response.json) > 0  # Meaning there's at least one building in the response


@pytest.mark.order(14)
def test_get_buildings_with_elevator_id(client):
    response = client.get('/building/get/2')
    assert response.status_code == 200
    assert len(response.json) > 0  # Meaning there's at least one building in the response


@pytest.mark.order(19)
def test_update_building(client):
    data = {
        "id": 2,
        "new_values": {
            "country": "Updated Country"
        }
    }
    response = client.put('/building/update', json=data)
    assert response.status_code == 200


@pytest.mark.order(26)
def test_delete_building(client):
    data = {
        "id": 2
    }
    response = client.delete('/building/delete', json=data)
    assert response.status_code == 200
