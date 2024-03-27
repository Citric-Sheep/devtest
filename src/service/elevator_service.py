import random
from datetime import datetime
from CRUD.CRUD import get_db_connection, get_trips, create_trip


class ElevatorService:
    def __init__(self):
        self.current_floor = 1  # Asumiendo que el ascensor comienza en el primer piso
        self.moving_direction = None  # 'up', 'down', o None

    def find_optimal_resting_floor(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT StartFloor, COUNT(StartFloor) as demand
            FROM ElevatorTrips
            GROUP BY StartFloor
            ORDER BY demand DESC
            LIMIT 1
        ''')
        result = cursor.fetchone()
        print(f"El conteo es de {result['StartFloor']}")
        conn.close()

        return result['StartFloor'] if result else self.current_floor

    def handle_call(self, call_floor):
        if call_floor == self.current_floor:
            print(f"El ascensor ya está en el piso {self.current_floor}. No necesita moverse.")
            return

        # Movimiento del ascensor
        print(f"El ascensor se está moviendo desde el piso {self.current_floor} al piso {call_floor}")
        start_time = datetime.now()
        self.moving_direction = 'up' if call_floor > self.current_floor else 'down'
        end_time = datetime.now()
        create_trip(self.current_floor, call_floor, start_time, end_time, True)
        self.current_floor = call_floor

        # Determinar y mover al piso óptimo de descanso después de atender la llamada
        optimal_floor = self.find_optimal_resting_floor()
        if self.current_floor != optimal_floor:
            print(f"El ascensor se moverá al piso óptimo de descanso {optimal_floor} después de atender la llamada")
            create_trip(self.current_floor, optimal_floor, datetime.now(), datetime.now(), False)
            self.current_floor = optimal_floor  # Actualizar el piso actual después de moverse al piso de descanso
