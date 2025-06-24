"""
Schemas para Demandas de Ascensor.

Estos modelos representan la estructura de los datos relacionados con las llamadas (demandas) al ascensor.
Pensé en dejar elevator_id como opcional para facilitar el desarrollo, pero en caso de escalar a múltiples ascensores debería volverse obligatorio.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class DemandBase(BaseModel):
    floor: int = Field(..., description="Piso donde ocurre la llamada")
    destination_floor: int = Field(..., description="Piso destino del usuario")
    elevator_id: Optional[int] = Field(1, description="Identificador del ascensor (por defecto 1)")

class DemandCreate(DemandBase):
    timestamp_called: Optional[datetime] = Field(
        None,
        description="Momento en que se registró la demanda; se autocompleta si no se envía."
    )

class DemandRead(DemandBase):
    id: int
    timestamp_called: datetime

    model_config = ConfigDict(from_attributes=True)
