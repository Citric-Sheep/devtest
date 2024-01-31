from typing import List
import uuid
from src.entities.smart_elevator import DemandLog
import json


class DemandLogDatabase:
    @staticmethod
    def create(log: DemandLog) -> str:
        log.id = str(uuid.uuid4())
        logs = DemandLogDatabase._load_data()
        logs.append(log.model_dump(mode="json"))
        DemandLogDatabase._save_data(logs)
        return str(log.id)

    @staticmethod
    def get_by_id(log_id: str) -> DemandLog:
        logs = DemandLogDatabase._load_data()
        for log_data in logs:
            if log_data["_id"] == log_id:
                return DemandLog(**log_data)
        return None

    @staticmethod
    def get_by_elevator_id(elevator_id: str) -> List[DemandLog]:
        logs = DemandLogDatabase._load_data()
        return [
            DemandLog(**log) for log in logs if log.get("elevator_id") == elevator_id
        ]

    @staticmethod
    def get_all() -> List[DemandLog]:
        logs = DemandLogDatabase._load_data()
        return [DemandLog(**log) for log in logs]

    @staticmethod
    def update(log: DemandLog) -> None:
        logs = DemandLogDatabase._load_data()
        for i, log_data in enumerate(logs):
            if log_data["_id"] == log.id:
                logs[i] = log.model_dump(mode="json")
                break
        DemandLogDatabase._save_data(logs)

    @staticmethod
    def delete(log_id: str) -> None:
        logs = DemandLogDatabase._load_data()
        logs = [log for log in logs if log["_id"] != log_id]
        DemandLogDatabase._save_data(logs)

    @staticmethod
    def _load_data() -> List[dict]:
        try:
            with open("demand_logs.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    @staticmethod
    def _save_data(data: List[dict]) -> None:
        with open("demand_logs.json", "w") as file:
            json.dump(data, file, indent=2)
