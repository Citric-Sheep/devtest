import sqlite3

def get_db_connection():
    db_path = r'database\elevator.db'  
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print('Conexión exitosa a la base de datos.')
        return conn
    except sqlite3.Error as error:
        print(f'Error al conectar a la base de datos: {error}')
        return None

def create_trip(start_floor, end_floor, start_time, end_time, is_demand):
    conn = None
    try:
        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ElevatorTrips (StartFloor, EndFloor, StartTime, EndTime, IsDemand)
                VALUES (?, ?, ?, ?, ?)
            ''', (start_floor, end_floor, start_time, end_time, is_demand))
            conn.commit()
            print("Viaje creado exitosamente.")
        else:
            print("No se pudo establecer conexión con la base de datos.")
    except Exception as error:
        print(f"Error al crear un viaje: {error}")
        if conn:
            conn.rollback()  # Deshacer los cambios si ocurre un error
    finally:
        if conn:
            conn.close()

def get_trips():
    conn = None
    try:
        conn = get_db_connection()
        if conn is not None:
            trips = conn.execute('SELECT * FROM ElevatorTrips').fetchall()
            return trips
        else:
            print("No se pudo establecer conexión con la base de datos.")
            return []
    except Exception as error:
        print(f"Error al obtener los viajes: {error}")
        return []
    finally:
        if conn:
            conn.close()

def update_trip(trip_id, end_floor):
    conn = None
    try:
        conn = get_db_connection()
        if conn is not None:
            conn.execute('''
                UPDATE ElevatorTrips
                SET EndFloor = ?
                WHERE TripID = ?
            ''', (end_floor, trip_id))
            conn.commit()
            print(f"Viaje actualizado exitosamente para el TripID {trip_id}.")
        else:
            print("No se pudo establecer conexión con la base de datos.")
    except Exception as error:
        print(f"Error al actualizar el viaje: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_trip(trip_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is not None:
            conn.execute('DELETE FROM ElevatorTrips WHERE TripID = ?', (trip_id,))
            conn.commit()
            print(f"Viaje con TripID {trip_id} eliminado exitosamente.")
        else:
            print("No se pudo establecer conexión con la base de datos.")
    except Exception as error:
        print(f"Error al eliminar el viaje: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
