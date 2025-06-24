"""
Tests para el endpoint de demandas (llamadas de ascensor).

puntos a testear para este endpoint:
-Validacion de pisos posibles
-Validacion de piso destino
-Cierre automatico del resting_period
-Que las demandas sean guardadas en sistema
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MIN_FLOOR = 1
MAX_FLOOR = 12

def test_create_demand_ok():
    """
    Prueba que se pueda crear una demanda en el piso mínimo permitido, con un destino válido.
    """
    payload = {
        "floor": MIN_FLOOR,
        "destination_floor": MIN_FLOOR + 1  # Un destino válido distinto al origen
    }
    response = client.post("/demands/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["floor"] == MIN_FLOOR
    assert data["destination_floor"] == MIN_FLOOR + 1
    assert "id" in data
    assert "timestamp_called" in data

def test_create_demand_out_of_range():
    """
    No debe aceptarse una demanda para un piso inexistente.
    """
    payload = {
        "floor": MAX_FLOOR + 1,
        "destination_floor": MIN_FLOOR
    }
    response = client.post("/demands/", json=payload)
    assert response.status_code == 400
    assert "El piso debe estar entre" in response.json()["detail"]

def test_create_demand_negative_floor():
    """
    Caso borde: piso negativo. 
    """
    payload = {
        "floor": -5,
        "destination_floor": MIN_FLOOR
    }
    response = client.post("/demands/", json=payload)
    assert response.status_code == 400

def test_create_demand_invalid_destination():
    """
    No debe aceptarse una demanda para un destino fuera de rango.
    """
    payload = {
        "floor": MIN_FLOOR,
        "destination_floor": MAX_FLOOR + 1
    }
    response = client.post("/demands/", json=payload)
    assert response.status_code == 400
    assert "piso destino" in response.json()["detail"]

def test_list_demands():
    """
    Comprueba que las demandas se acumulen en el sistema.
    """
    client.post("/demands/", json={"floor": MIN_FLOOR, "destination_floor": MIN_FLOOR + 1})
    client.post("/demands/", json={"floor": MAX_FLOOR, "destination_floor": MIN_FLOOR})
    response = client.get("/demands/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Al menos dos demandas deben haberse registrado.
    assert len(data) >= 2

def test_resting_is_closed_on_demand():
    """
    Prueba que al crear una demanda se cierra automáticamente el último resting abierto.
    """
    # Abrimos un resting_period manualmente.
    client.post("/resting_periods/", json={"floor": MIN_FLOOR})
    # Ahora creamos una demanda, que debería cerrar el resting.
    response = client.post("/demands/", json={"floor": MIN_FLOOR, "destination_floor": MIN_FLOOR + 1})
    assert response.status_code == 200
    # Revisamos que el último resting_period tenga resting_end no nulo.
    response = client.get("/resting_periods/")
    restings = response.json()
    assert restings[-1]["resting_end"] is not None
