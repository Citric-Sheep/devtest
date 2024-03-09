# from fastapi import APIRouter, Depends, HTTPException
# from . import models
# from sqlalchemy.orm import Session
# from . import schemas
# from .db import SessionLocal
# import datetime
# import pandas as pd

from fastapi import APIRouter, Depends, HTTPException
import models
from sqlalchemy.orm import Session
import schemas
from db import SessionLocal
import datetime
import pandas as pd
from pydantic import BaseModel
from typing import Optional, List, Dict, Union

router = APIRouter()

'''
+++++++++++++++++++++++++++++                           +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   DEPENDENCY INJECTION    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++          FOR DB           +++++++++++++++++++++++++++++
'''
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   CREATE ELEVATOR MOVEMENTS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
'''
@router.post("/elevator_movement/", response_model=schemas.ElevatorMovement)
def create_elevator_movement(elevator_movement: schemas.ElevatorMovementCreate, db: Session = Depends(get_db)):
    if elevator_movement.action == "move":
        current_floor = elevator_movement.current_floor
        next_floor = elevator_movement.next_floor

        # Verificar la secuencia cronológica
        if next_floor == current_floor:
            raise HTTPException(status_code=400, detail="floor selected is currently the rest floor")
        
        # Definir el límite superior del ascensor (piso 10) y el límite inferior (piso 1)
        top_floor = 10
        bottom_floor = 1

        # Verificar si el ascensor está subiendo o bajando
        if next_floor > current_floor:
            # Si está subiendo, verificar que el siguiente piso no supere el límite superior
            if next_floor > top_floor:
                raise HTTPException(status_code=400, detail=f"Next floor cannot exceed top floor ({top_floor})")
        else:
            # Si está bajando, verificar que el siguiente piso no sea menor que el límite inferior
            if next_floor < bottom_floor:
                raise HTTPException(status_code=400, detail=f"Next floor cannot be below bottom floor ({bottom_floor})")
        
        # Lógica para calcular el tiempo y la hora de llegada esperada
        time_between_floors = abs(next_floor - current_floor) * 10  # 10 segundos por piso
        expected_arrival_time = datetime.datetime.now() + datetime.timedelta(seconds=time_between_floors)

        # Actualizar la información en la base de datos
        db_elevator_movement = models.ElevatorMovement(**elevator_movement.model_dump())
        db.add(db_elevator_movement)
        db.commit()
        db.refresh(db_elevator_movement)

        return db_elevator_movement

    elif elevator_movement.action == "call":
        # Implement logic for handling elevator call when it's vacant
        current_floor = elevator_movement.current_floor
        floor_requested = elevator_movement.floor_requested
       
       
        # Determine optimal resting floor based on current demand, historical data, etc.
        # optimal_resting_floor = calculate_optimal_resting_floor(current_floor, floor_requested)
        # Update elevator resting floor in the database
        # update_elevator_resting_floor(optimal_resting_floor)
        # Update elevator movement information in the database

    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    db_elevator_movement = models.ElevatorMovement(**elevator_movement.model_dump())
    db.add(db_elevator_movement)
    db.commit()
    db.refresh(db_elevator_movement)
   
    return db_elevator_movement



'''
+++++++++++++++++++++++++++++                               +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   ELEVATOR MOVEMENTS by ID    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                               +++++++++++++++++++++++++++++
'''
@router.get("/elevator_movement/{elevator_movement_id}", response_model=schemas.ElevatorMovement)
def read_elevator_movement(elevator_movement_id: int,
                            db: Session = Depends(get_db)):
    db_elevator_movement = db.query(models.ElevatorMovement).filter(models.ElevatorMovement.id == elevator_movement_id).first()
    if db_elevator_movement is None:
        raise HTTPException(status_code=404, detail="Elevator Movement not found")
    return db_elevator_movement
'''
+++++++++++++++++++++++++++++                         +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   ELEVATOR MOVEMENTS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                         +++++++++++++++++++++++++++++
'''
@router.get("/elevator_movements/", response_model=list[schemas.ElevatorMovement])
async def read_elevator_movements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Verificar que db sea una instancia válida de Session
    if not isinstance(db, Session):
        raise HTTPException(status_code=500, detail="Invalid database session")
    
    # Utilizar la sesión para realizar la consulta
    return db.query(models.ElevatorMovement).offset(skip).limit(limit).all()

'''
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   UPDATE ELEVATOR MOVEMENTS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
'''
@router.put("/elevator_movement/{elevator_movement_id}", response_model=schemas.ElevatorMovement)
def update_elevator_movement(elevator_movement_id: int, elevator_movement: schemas.ElevatorMovementUpdate, db: Session = Depends(get_db)):
    db_elevator_movement = db.query(models.ElevatorMovement).filter(models.ElevatorMovement.id == elevator_movement_id).first()
    if db_elevator_movement is None:
        raise HTTPException(status_code=404, detail="Elevator Movement not found")
    for key, value in elevator_movement.model_dump().items():
        setattr(db_elevator_movement, key, value)
    db.commit()
    db.refresh(db_elevator_movement)
    return db_elevator_movement
'''
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   DELETE ELEVATOR MOVEMENTS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                                +++++++++++++++++++++++++++++
'''
@router.delete("/elevator_movement/{elevator_movement_id}")
def delete_elevator_movement(elevator_movement_id: int, db: Session = Depends(get_db)):
    db_elevator_movement = db.query(models.ElevatorMovement).filter(models.ElevatorMovement.id == elevator_movement_id).first()
    if db_elevator_movement is None:
        raise HTTPException(status_code=404, detail="Elevator Movement not found")
    db.delete(db_elevator_movement)
    db.commit()
    return {"message": "Elevator Movement deleted successfully"}





'''
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   POST DEMAND   +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
'''
@router.post("/demand/", response_model=schemas.Demand)
def create_demand(demand: schemas.DemandCreate, db: Session = Depends(get_db)):
    db_demand = models.Demand(**demand.model_dump())
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand
'''
+++++++++++++++++++++++++++++                       +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   GET DEMAND BY ID    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                       +++++++++++++++++++++++++++++
'''
@router.get("/demand/{demand_id}", response_model=schemas.Demand)
def read_demand(demand_id: int, db: Session = Depends(get_db)):
    db_demand = db.query(models.Demand).filter(models.Demand.id == demand_id).first()
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    return db_demand

'''
+++++++++++++++++++++++++++++                  +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   GET DEMANDS    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                  +++++++++++++++++++++++++++++
'''
@router.get("/demands/", response_model=list[schemas.Demand])
def read_demands(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Demand).offset(skip).limit(limit).all()

'''
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   PUT DEMAND    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
'''
@router.put("/demand/{demand_id}", response_model=schemas.Demand)
def update_demand(demand_id: int, demand: schemas.DemandUpdate, db: Session = Depends(get_db)):
    db_demand = db.query(models.Demand).filter(models.Demand.id == demand_id).first()
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    for key, value in demand.model_dump().items():
        setattr(db_demand, key, value)
    db.commit()
    db.refresh(db_demand)
    return db_demand
'''
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   DEL DEMAND    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++
'''
@router.delete("/demand/{demand_id}")
def delete_demand(demand_id: int, db: Session = Depends(get_db)):
    db_demand = db.query(models.Demand).filter(models.Demand.id == demand_id).first()
    if db_demand is None:
        raise HTTPException(status_code=404, detail="Demand not found")
    db.delete(db_demand)
    db.commit()
    return {"message": "Demand deleted successfully"}


'''
+++++++++++++++++++++++++++++                +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++   PREDICTOR    +++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++                +++++++++++++++++++++++++++++
'''
# Endpoint para obtener el DataFrame construido
class FloorData(BaseModel):
    floor: int
    stops: Optional[int]
    demand: Optional[int]

class PreprocessingResponse(BaseModel):
    dataframe: List[FloorData]

@router.get("/predictor/preprocessing", response_model=PreprocessingResponse)
def get_dataframe(db: Session = Depends(get_db), min_stops: Optional[int] = 1):
    # Obtener datos de movimientos del ascensor y demandas de usuarios
    elevator_movements = read_elevator_movements(db)
    demands = read_demands(db)

    # Crear DataFrames a partir de los datos obtenidos
    elevator_movements_df = pd.DataFrame(elevator_movements)
    demands_df = pd.DataFrame(demands)

    # Calcular la cantidad de paradas por piso
    stops_per_floor = elevator_movements_df.groupby('next_floor').size().reset_index(name='stops')

    # Calcular la cantidad de demandas por piso
    demand_per_floor = demands_df.groupby('floor_requested').size().reset_index(name='demand')

    # Merge de los DataFrames
    merged_df = pd.merge(stops_per_floor, demand_per_floor, how='outer', left_on='next_floor', right_on='floor_requested')

    # Filtrar los pisos con un mínimo de paradas
    filtered_df = merged_df[merged_df['stops'] >= min_stops]

    # Obtener el piso con la mayor cantidad de paradas
    preferred_resting_floor = filtered_df.loc[filtered_df['stops'].idxmax()]['next_floor']

    # Combine the stops and demands data into FloorData objects
    floor_data = [FloorData(floor=row['next_floor'], stops=row['stops'], demand=row['demand']) for _, row in filtered_df.iterrows()]


    return PreprocessingResponse(dataframe=floor_data)