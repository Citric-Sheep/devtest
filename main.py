import random
from src.mongo_database import MongoDatabase
import os
import dotenv
from src.elevator import Elevator
from src.person import Person
def setup():
    dotenv.load_dotenv()
    mongo_connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    database = MongoDatabase(mongo_connection_string, 'CitricSheep', 'ElevatorHistory')

    elevator = Elevator()

    return database, elevator

def main():
    database, elevator = setup()

    names = ['John', 'Jane', 'Jack', 'Jill', 'James', 'Jenny', 'Jasper', 'Jade', 'Jared', 'Jasmine']
    n_entries = int(input("Enter number of entries: "))
    for _ in range(n_entries):
        floor_number = random.randint(0, 10)
        passengers = [Person(random.choice(names), random.randint(50,130)) for _ in range(random.randint(0, 10))]
        elevator_history_entry = elevator(int(floor_number), passengers)
        database.create(elevator_history_entry)
    
    print("Elevator history:")
    for elevator_history_entry in database.read_all_sorted():
        print(elevator_history_entry)
    
if __name__ == '__main__':
    main()