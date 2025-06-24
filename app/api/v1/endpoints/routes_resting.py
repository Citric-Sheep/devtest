"""
Endpoints para registrar periodos de descanso (idle) del ascensor.

Incluye validaciones realistas de dominio:
- El piso debe estar dentro del rango permitido.
- El periodo de descanso no puede finalizar antes de iniciar.

Decisión: Mantener los datos limpios facilita el futuro análisis y entrenamiento de modelos ML.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.resting_period import RestingPeriodCreate, RestingPeriodRead
from app.db.models import RestingPeriod
from app.db.db import get_db
from datetime import datetime, timezone

router = APIRouter()

# Rango de pisos permitido para este edificio (igual que en demandas).
MIN_FLOOR = 1
MAX_FLOOR = 12

@router.post("/resting_periods/", response_model=RestingPeriodRead)
def create_resting_period(period: RestingPeriodCreate, db: Session = Depends(get_db)):
    """
    Registra un periodo de descanso del ascensor.
    - Valida rango de piso.
    - Valida coherencia temporal (resting_end >= resting_start).
    """
    if period.floor < MIN_FLOOR or period.floor > MAX_FLOOR:
        raise HTTPException(
            status_code=400,
            detail=f"El piso debe estar entre {MIN_FLOOR} y {MAX_FLOOR}."
        )
    # Si se ingresa resting_end, debe ser igual o posterior a resting_start (o a ahora si no se da inicio).
    resting_start = period.resting_start or datetime.now(timezone.utc)
    if period.resting_end and period.resting_end < resting_start:
        raise HTTPException(
            status_code=400,
            detail="El final del periodo de descanso no puede ser anterior al inicio."
        )
    db_period = RestingPeriod(
        elevator_id=period.elevator_id,
        floor=period.floor,
        resting_start=resting_start,
        resting_end=period.resting_end
    )
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period

@router.get("/resting_periods/", response_model=list[RestingPeriodRead])
def list_resting_periods(db: Session = Depends(get_db)):
    """
    Lista todos los periodos de descanso registrados.
    Esto es útil para análisis y debugging del flujo del ascensor.
    """
    return db.query(RestingPeriod).all()

# NOTA: En sistemas reales, sería interesante agregar endpoint PATCH para cerrar un periodo idle abierto cuando el ascensor recibe una demanda.
# TODO: Agregar validación para evitar superposición de periodos resting abiertos para el mismo ascensor.
