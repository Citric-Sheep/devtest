from app.db.models import Demand, RestingPeriod
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

def create_resting_period(db: Session, elevator_id: int, floor: int, resting_start: datetime, resting_end: Optional[datetime]):
    """
    Crea y guarda un periodo de descanso.
    Validación extra podría añadirse aquí si cambian las reglas del dominio.
    """
    rp = RestingPeriod(
        elevator_id=elevator_id,
        floor=floor,
        resting_start=resting_start,
        resting_end=resting_end,
    )
    db.add(rp)
    db.commit()
    db.refresh(rp)
    return rp

def create_demand(db: Session, elevator_id: int, destination_floor: int, floor: int, timestamp_called: datetime):
    """
    Crea y guarda una demanda (llamada de ascensor).
    Esta función podría ampliarse en el futuro para cerrar resting_periods automáticamente.
    """
    d = Demand(
        elevator_id=elevator_id,
        floor=floor,
        destination_floor=destination_floor,
        timestamp_called=timestamp_called,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d
