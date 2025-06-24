"""
Script para poblar la base con datos artificiales, simulando la lógica de uso real de un ascensor.

- Más actividad en horario laboral.
- Descansos más largos en pisos intermedios.
- Llamadas simuladas según patrones horarios (mañana suben, tarde bajan).
- Usa helpers para mantener la lógica de negocio centralizada.

Esto permite testear todo el pipeline y entrenar un futuro modelo ML.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.data_utils import create_resting_period, create_demand
from datetime import datetime, timedelta
import random
import os

DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://devsaieh:saiehpass@localhost:5433/devtest_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

MIN_FLOOR = 1
MAX_FLOOR = 12

def random_resting_floor(hour):
    if hour < 7 or hour > 20:
        return MIN_FLOOR
    return random.choice(range(2, MAX_FLOOR))

def random_demand(hour):
    if 8 <= hour < 10:
        return MIN_FLOOR, random.randint(2, MAX_FLOOR)
    elif 17 <= hour < 19:
        return random.randint(2, MAX_FLOOR), MIN_FLOOR
    else:
        piso_from = random.randint(MIN_FLOOR, MAX_FLOOR)
        piso_to = random.randint(MIN_FLOOR, MAX_FLOOR)
        while piso_to == piso_from:
            piso_to = random.randint(MIN_FLOOR, MAX_FLOOR)
        return piso_from, piso_to

def generate_fake_data(days=5, seed=42):
    random.seed(seed)
    session = Session()
    base_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    for day in range(days):
        curr_time = base_date + timedelta(days=day)
        for i in range(10, 22):  # Simula actividad diurna y vespertina
            curr_hour = curr_time.replace(hour=i)
            # 1. Registra resting_period
            resting_floor = random_resting_floor(i)
            resting_start = curr_hour
            resting_end = curr_hour + timedelta(minutes=random.randint(2, 8))
            create_resting_period(
                db=session,
                elevator_id=1,
                floor=resting_floor,
                resting_start=resting_start,
                resting_end=resting_end
            )
            # 2. Registra 1-2 demandas luego del descanso
            for _ in range(random.randint(1, 2)):
                from_floor, to_floor = random_demand(i)
                demand_time = resting_end + timedelta(minutes=random.randint(1, 5))
                create_demand(
                    db=session,
                    elevator_id=1,
                    floor=from_floor,
                    destination_floor=to_floor,  
                    timestamp_called=demand_time
                )
    session.close()
    print(f"Datos artificiales generados para {days} días.")

if __name__ == "__main__":
    generate_fake_data(days=7)
