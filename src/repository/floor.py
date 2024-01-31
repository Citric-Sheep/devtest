from src.repository.interface import BaseRepository


class FloorRepository(BaseRepository):
    def add(self, floor):
        self.db_session.add(floor)
        self.db_session.commit()
        self.db_session.refresh(floor)
        return floor

    def get(self, model, floor_id):
        return self.db_session.query(model).filter(model.id == floor_id).first()