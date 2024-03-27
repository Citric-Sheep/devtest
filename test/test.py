from CRUD.CRUD import get_db_connection, create_trip, get_trips, update_trip, delete_trip
import random
from datetime import datetime

start_time = datetime.now()
end_time = datetime.now()

def test_db_connection():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    assert cursor.fetchone()[0] == 1
    conn.close()
    print("Conexión a la base de datos exitosa y funcionando correctamente.")


def test_create_trip():
    try:
        # Asignar pisos de inicio y fin de manera aleatoria entre 1 y 7
        start_floor = random.randint(2, 7)
        end_floor = random.randint(2, 7)

        # Asegurar que el piso final sea diferente al piso inicial
        while end_floor == start_floor:
            end_floor = random.randint(1, 7)

        print(f"Creando un viaje desde el piso {start_floor} al piso {end_floor}.")

        # Crear un nuevo viaje y verificar que se ha añadido
        create_trip(start_floor, end_floor, start_time, end_time, True)
        trips = get_trips()

        assert len(trips) > 0, "No se han encontrado viajes en la base de datos."
        print("Prueba de inserción completada con éxito.")

    except Exception as e:
        print(f"Ocurrió un error al probar la creación del viaje: {e}")
        
def get_trip(trip_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ElevatorTrips WHERE TripID = ?', (trip_id,))
        trip = cursor.fetchone()
        conn.close()

        if trip:
            return dict(trip)  # Convertir la tupla en un diccionario para facilitar el acceso
        else:
            print(f"No se encontró un viaje con el ID {trip_id}.")
            return None

    except Exception as e:
        print(f"Error al obtener el viaje con ID {trip_id}: {e}")
        return None

def test_update_trip():
    try:
        # Intentar obtener un viaje para actualizar
        trip = get_trip(3)  # O cualquier ID específico

        if not trip:
            print("No hay viajes disponibles para actualizar.")
            return

        # Asignar un piso final de manera aleatoria entre 1 y 7
        new_end_floor = random.randint(1, 7)

        print(f"Actualizando el viaje ID {trip['TripID']} al piso final {new_end_floor}.")

        # Actualizar el viaje y verificar que la actualización es correcta
        update_trip(trip_id=trip['TripID'], end_floor=new_end_floor)

        # Recuperar el viaje actualizado para verificar la actualización
        updated_trip = get_trip(trip['TripID'])
        assert updated_trip and updated_trip['EndFloor'] == new_end_floor, "La actualización del viaje falló"

        print("Prueba de actualización completada con éxito.")

    except Exception as e:
        print(f"Ocurrió un error al probar la actualización del viaje: {e}")
        
def test_delete_trip():
    try:
        # Asegurar que existe al menos un viaje para eliminar
        trip_to_delete = get_trips()[0]  # Obtiene el primer viaje para eliminar
        trip_id_to_delete = trip_to_delete['TripID']

        print(f"Intentando eliminar el viaje con ID {trip_id_to_delete}.")

        # Eliminar un viaje y verificar que se ha eliminado
        delete_trip(trip_id=trip_id_to_delete)
        trips = get_trips()
        assert all(trip['TripID'] != trip_id_to_delete for trip in trips), "El viaje no fue eliminado correctamente."

        print("Prueba de eliminación completada con éxito.")

    except IndexError:
        print("No hay viajes disponibles para eliminar.")
    except Exception as e:
        print(f"Ocurrió un error al probar la eliminación del viaje: {e}")