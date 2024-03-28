import pytest
from server import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.order(4)
def test_create_elevator(client):
    data = {
        "custom_id": 2,
        "building_id": 2,
        "max_floors": 5,
        "local_identifier": 3
    }
    response = client.post('/elevator/create', json=data)
    assert response.status_code == 201


@pytest.mark.order(10)
def test_get_elevators(client):
    response = client.get('/elevator/get')
    assert response.status_code == 200


@pytest.mark.order(16)
def test_get_elevators_with_building_id(client):
    response = client.get('/elevator/get/2')
    assert response.status_code == 200


@pytest.mark.order(20)
def test_update_elevator(client):
    data = {
        "id": 2,
        "new_values": {
            "local_identifier": 4
        }
    }
    response = client.put('/elevator/update', json=data)
    assert response.status_code == 200


@pytest.mark.order(24)
def test_delete_elevator(client):
    data = {
        "id": 2
    }
    response = client.delete('/elevator/delete', json=data)
    assert response.status_code == 200
    