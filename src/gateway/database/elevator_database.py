import json
import uuid
from typing import List

from src.entities.smart_elevator import SmartElevator


class ElevatorDatabase:
    @staticmethod
    def create(elevator: SmartElevator) -> str:
        elevator.id = str(uuid.uuid4())
        elevators = ElevatorDatabase._load_data()
        elevators.append(elevator.model_dump(mode="json"))
        ElevatorDatabase._save_data(elevators)
        return str(elevator.id)

    @staticmethod
    def get_by_id(elevator_id: str) -> SmartElevator:
        elevators = ElevatorDatabase._load_data()
        for elevator_data in elevators:
            if elevator_data["id"] == elevator_id:
                return SmartElevator(**elevator_data)
        return None

    @staticmethod
    def get_all() -> List[SmartElevator]:
        elevators = ElevatorDatabase._load_data()
        return [SmartElevator(**elevator) for elevator in elevators]

    @staticmethod
    def update(elevator: SmartElevator) -> None:
        elevators = ElevatorDatabase._load_data()
        for i, elevator_data in enumerate(elevators):
            if elevator_data["id"] == elevator.id:
                elevators[i] = elevator.model_dump(mode="json")
                break
        ElevatorDatabase._save_data(elevators)

    @staticmethod
    def delete(elevator_id: str) -> None:
        elevators = ElevatorDatabase._load_data()
        elevators = [
            elevator for elevator in elevators if elevator["id"] != elevator_id
        ]
        ElevatorDatabase._save_data(elevators)

    @staticmethod
    def _load_data() -> List[dict]:
        try:
            with open("elevators.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    @staticmethod
    def _save_data(data: List[dict]) -> None:
        with open("elevators.json", "w") as file:
            json.dump(data, file, indent=2)
