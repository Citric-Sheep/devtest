from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app, get_db
from src.database import Base
from generators import generate_event_sequence


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_event():

    payload = {
        "event_type": "door_opened",
        "current_floor": 0,
        "target_floor": 0,
        "load": 0,
        "is_vacant": True,
        "captured_at": "2019-08-24T14:15:22Z",
        "elevator_id": 0
    }

    response = client.post("/event/",json=payload
                           )
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "door_opened"
    assert "elevator_id" in data
    elevator_id = data["elevator_id"]

    response = client.get(f"/events/{elevator_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data)==1
    assert data[0]['elevator_id'] == elevator_id
    assert data[0]['captured_at'] == "2019-08-24T14:15:22"

def test_list_events():
    
    sequence_length = 15
    elevator_id = 1

    for payload in generate_event_sequence(sequence_length, elevator_id):
        response = client.post("/event/",json=payload)
        assert response.status_code == 200

    response = client.get(f"/events/{elevator_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data)==sequence_length



