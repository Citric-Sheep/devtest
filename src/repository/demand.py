from src.repository.interface import BaseRepository


class DemandRepository(BaseRepository):
    def add(self, demand):
        self.db_session.add(demand)
        self.db_session.commit()
        self.db_session.refresh(demand)
        return demand

    def get(self, model, demand_id):
        return self.db_session.query(model).filter(model.id == demand_id).first()