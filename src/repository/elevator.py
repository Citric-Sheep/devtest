from src.repository.interface import BaseRepository


class ElevatorRepository(BaseRepository):
    def add(self, elevator):
        self.db_session.add(elevator)
        self.db_session.commit()
        self.db_session.refresh(elevator)
        return elevator

    def get(self, model, elevator_id):
        return self.db_session.query(model).filter(model.id == elevator_id).first()