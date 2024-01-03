import random
from src.schemas import EventType
from datetime import datetime, timedelta


def generate_event_sequence(length: int = 10, elevator_id = None):

    events = [{
        "event_type": random.choice(list(EventType)).value,
        "current_floor": random.randint(1,10),
        "target_floor": random.randint(1,10),
        "load": int(random.uniform(0,600)),
        "is_vacant": random.uniform(0,2)>1,
        "captured_at": (datetime.now() - timedelta(seconds=random.uniform(0, 3600))).isoformat(),
        "elevator_id": elevator_id or random.choice(1,5)
    } for i in range(length)]

    return events