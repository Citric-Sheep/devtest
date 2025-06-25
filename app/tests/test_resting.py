"""
Tests para endpoint de periodos de descanso (resting_periods).

Incluye validaciones de negocio y casos raros, simulando errores comunes de usuarios o carga manual.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MIN_FLOOR = 1
MAX_FLOOR = 12

def test_create_resting_ok():
    """
    Test simple: crear un resting_period válido en el piso más bajo.
    """
    payload = {"floor": MIN_FLOOR}
    response = client.post("/resting_periods/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["floor"] == MIN_FLOOR
    assert "id" in data

def test_create_resting_out_of_range():
    """
    No se debe aceptar un resting en un piso que no existe.
    Suele pasar si hay un error en los sensores del sistema físico.
    """
    payload = {"floor": MAX_FLOOR + 1}
    response = client.post("/resting_periods/", json=payload)
    assert response.status_code == 400

def test_create_resting_end_before_start():
    """
    Caso de error de ingreso manual: el tiempo de término no puede ser anterior al de inicio.
    """
    from datetime import datetime, timedelta
    start = datetime.now().isoformat()
    end = (datetime.now() - timedelta(minutes=10)).isoformat()
    payload = {
        "floor": MIN_FLOOR,
        "resting_start": start,
        "resting_end": end
    }
    response = client.post("/resting_periods/", json=payload)
    assert response.status_code == 400
    assert "no puede ser anterior" in response.json()["detail"]

def test_list_restings():
    """
    Asegura que los periodos de descanso se almacenan correctamente y pueden ser consultados.
    """
    client.post("/resting_periods/", json={"floor": MIN_FLOOR})
    response = client.get("/resting_periods/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
