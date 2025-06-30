from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_demand():
    resp = client.post("/api/demands", json={"floor": 3})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["floor"] == 3
    assert "id" in payload
    assert "timestamp" in payload


def test_create_state():
    resp = client.post("/api/state", json={"floor": 2, "vacant": True})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["floor"] == 2
    assert payload["vacant"] is True
    assert "timestamp" in payload


def test_analyze_positioning():
    # Criar um state antigo
    client.post("/api/state", json={"floor": 1, "vacant": True})

    # Criar uma demanda posterior
    client.post("/api/demands", json={"floor": 5})

    # Chamar a rota de análise
    resp = client.get("/api/analytics", params={"limit": 10, "threshold": 2})
    assert resp.status_code == 200
    data = resp.json()

    assert "average_distance" in data
    assert "mispositioned" in data
    assert isinstance(data["average_distance"], float)
    assert isinstance(data["mispositioned"], bool)