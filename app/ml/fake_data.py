from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.data_utils import create_resting_period, create_demand
from datetime import datetime, timedelta
import random
import os
import numpy as np

DATABASE_URL = os.environ.get("DATABASE_URL") or "postgresql://devsaieh:saiehpass@localhost:5433/devtest_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

MIN_FLOOR = 1
MAX_FLOOR = 12

def random_resting_floor(hour, is_weekend):
    """
    En fines de semana, el ascensor descansa más tiempo en el lobby.
    """
    if hour < 7 or hour > 20:
        return MIN_FLOOR
    if is_weekend:
        return MIN_FLOOR if random.random() < 0.7 else random.choice(range(2, MAX_FLOOR))
    # Días de semana: intermedio
    return random.choice(range(2, MAX_FLOOR))

def random_demand(hour, is_weekend):
    """
    Días de semana: patrones normales.
    Fines de semana: menos tráfico, más viajes entre pisos bajos.
    """
    if is_weekend:
        # Menos tráfico y la mayoría son entre pisos bajos.
        if random.random() < 0.8:
            piso_from = random.choice([MIN_FLOOR, 2, 3])
            piso_to = random.choice([MIN_FLOOR, 2, 3])
            while piso_to == piso_from:
                piso_to = random.choice([MIN_FLOOR, 2, 3])
            return piso_from, piso_to
        else:
            piso_from = random.randint(MIN_FLOOR, MAX_FLOOR)
            piso_to = random.randint(MIN_FLOOR, MAX_FLOOR)
            while piso_to == piso_from:
                piso_to = random.randint(MIN_FLOOR, MAX_FLOOR)
            return piso_from, piso_to

    # Días de semana: patrón original
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

def generate_fake_data(days=7, seed=42):
    """
    Genera datos artificiales para 'days' días seguidos, con fines de semana diferenciados.
    """
    random.seed(seed)
    np.random.seed(seed)
    session = Session()
    base_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    for day in range(days):
        curr_time = base_date + timedelta(days=day)
        weekday = curr_time.weekday()
        is_weekend = weekday >= 5  # sábado=5, domingo=6

        for i in range(10, 22):  # 10:00 a 21:00
            curr_hour = curr_time.replace(hour=i)
            # 1. Resting period
            resting_floor = random_resting_floor(i, is_weekend)
            resting_start = curr_hour
            resting_duration = random.randint(5, 14) if is_weekend else random.randint(2, 8)
            resting_end = curr_hour + timedelta(minutes=resting_duration)
            create_resting_period(
                db=session,
                elevator_id=1,
                floor=resting_floor,
                resting_start=resting_start,
                resting_end=resting_end
            )
            # 2. Número de demandas menor en finde
            n_demands = random.randint(0, 1) if is_weekend else random.randint(1, 2)
            last_time = resting_end
            for _ in range(n_demands):
                from_floor, to_floor = random_demand(i, is_weekend)
                # Tiempo entre descansos y demanda: exponencial (más realista)
                minutes = int(np.random.exponential(scale=3))
                demand_time = last_time + timedelta(minutes=max(1, minutes))
                last_time = demand_time
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
    generate_fake_data(days=31)
