import unittest
from CRUD.CRUD import create_trip, get_trips, update_trip, delete_trip
from src.service.elevator_service import ElevatorService

class TestElevatorCRUD(unittest.TestCase):
    def test_create_and_get_trip(self):
        create_trip(1, 5, '2022-01-01 10:00:00', '2022-01-01 10:05:00', True)
        trips = get_trips()
        self.assertGreater(len(trips), 0)

    def test_update_trip(self):
        initial_end_floor = 6
        new_end_floor = 7
        create_trip(1, initial_end_floor, '2022-01-01 10:00:00', '2022-01-01 10:05:00', True)  # Asegura que hay un viaje para actualizar
        trips = get_trips()
        trip_id_to_update = trips[0]['TripID']  # Asume que el viaje que queremos actualizar es el primero
        update_trip(trip_id_to_update, new_end_floor)
        updated_trip = next((trip for trip in get_trips() if trip['TripID'] == trip_id_to_update), None)
        self.assertIsNotNone(updated_trip)
        self.assertEqual(updated_trip['EndFloor'], new_end_floor)

    def test_delete_trip(self):
        delete_trip(trip_id=1)
        trips = get_trips()
        self.assertNotIn(1, [trip['TripID'] for trip in trips])
        
class TestElevatorService(unittest.TestCase):
    def setUp(self):
        self.elevator_service = ElevatorService()

    def test_handle_call(self):
        self.elevator_service.handle_call(3)
        self.assertEqual(self.elevator_service.current_floor, 3 )

    def test_find_optimal_resting_floor(self):
        optimal_floor = self.elevator_service.find_optimal_resting_floor()
        # El valor esperado dependerá de los datos en tu base de datos de prueba
        self.assertIn(optimal_floor, [1, 2, 3, 4, 5, 6, 7])