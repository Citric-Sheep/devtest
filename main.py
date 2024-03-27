from test.test import test_db_connection, test_create_trip, test_update_trip, test_delete_trip
from CRUD.CRUD import get_db_connection
from src.service.elevator_service import ElevatorService
import unittest

#test_db_connection()
#test_create_trip()
#test_update_trip()
#test_delete_trip()


def main():
    elevator_service = ElevatorService()

    # Simula algunas llamadas al ascensor
    elevator_service.handle_call(7)
    #elevator_service.handle_call(2)
    #for i in range(1,100):
    #    test_create_trip()
        
    # A continuación, el código para ejecutar las pruebas unitarias
    loader = unittest.TestLoader()
    suite = loader.discover('D:\\RED\\PruebasTecnicas\\CitricSheep\\test', pattern='unit_test.py')

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main()