"""
Endpoints para manejar las demandas (llamadas) del ascensor.

Incluye lógica de negocio que cierra automáticamente el último resting_period abierto
para el ascensor cuando se recibe una nueva demanda, y validaciones realistas de dominio.

Decisión de diseño: validamos rango de piso para evitar datos corruptos y reflejar la realidad física del edificio.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.demand import DemandCreate, DemandRead
from app.db.models import Demand, RestingPeriod
from app.db.db import get_db
from datetime import datetime, timezone

router = APIRouter()

# Defino el rango de pisos permitido. TODO: parametrizar esto según configuración por edificio.
MIN_FLOOR = 1
MAX_FLOOR = 12

@router.post("/demands/", response_model=DemandRead)
def create_demand(demand: DemandCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva demanda de ascensor.
    - Valida que el piso esté en rango permitido.
    - Cierra el último resting_period abierto (sin resting_end) para el ascensor, si existe.
    """
    # Validación de piso: no se permiten pisos fuera de rango (ejemplo: sótanos o pisos inexistentes).
    if demand.destination_floor < MIN_FLOOR or demand.destination_floor > MAX_FLOOR:
        raise HTTPException(
            status_code=400,
            detail=f"El piso destino debe estar entre {MIN_FLOOR} y {MAX_FLOOR}."
        )

    # Al registrar una demanda, cerramos automáticamente el resting actual (idle) si existe.
    last_resting = db.query(RestingPeriod).filter(
        RestingPeriod.elevator_id == demand.elevator_id,
        RestingPeriod.resting_end.is_(None)
    ).order_by(RestingPeriod.resting_start.desc()).first()

    if last_resting:
        # Usamos el mismo timestamp de la demanda para cerrar el periodo idle.
        last_resting.resting_end = demand.timestamp_called or datetime.now(timezone.utc)
        db.add(last_resting)
        # Comentario: Esto ayuda a mantener coherencia temporal entre resting y demanda.

    db_demand = Demand(
        elevator_id=demand.elevator_id,
        floor=demand.floor,
        destination_floor=demand.destination_floor,  # NUEVO
        timestamp_called=demand.timestamp_called or datetime.now(timezone.utc)
    )

    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand

@router.get("/demands/", response_model=list[DemandRead])
def list_demands(db: Session = Depends(get_db)):
    """
    Lista todas las demandas registradas.
    Pensado para debug y análisis histórico.
    """
    return db.query(Demand).all()
