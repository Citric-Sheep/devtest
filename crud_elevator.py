from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime
from create_table import ElevatorState
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import desc


# Create a session
class ElevatorStateManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_elevator_state(self, current_floor, demand_floor,next_floor,date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        new_state = ElevatorState(current_floor=current_floor, demand_floor=demand_floor,next_floor= next_floor, call_datetime= date)
        self.session.add(new_state)
        self.session.commit()
        return new_state
    def get_last_elevator_state(self):
        # Query the database to get the last row based on the ID in descending order
        last_state = self.session.query(ElevatorState).order_by(desc(ElevatorState.id)).first()
        return last_state
    def get_all_elevator_states(self):
        return self.session.query(ElevatorState).all()

    def update_elevator_state_state(self, state_id, current_floor):
        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            state.current_floor = current_floor
            self.session.commit()
            return state  # Return the updated state
        else:
            print(f"No state found with id={state_id}. Count: {self.session.query(ElevatorState).filter_by(id=state_id).count()}")
        return None  # Return None if 

    def delete_elevator_state(self, state_id):
        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            self.session.delete(state)
            self.session.commit()
            
    def delete_all_elevator_states(self):
        try:
            self.session.query(ElevatorState).delete()
            self.session.commit()
            print("All rows deleted successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting all rows: {e}")
            
if __name__ == "__main__":
        # Example usage
    manager = ElevatorStateManager(database_url="postgresql://postgres:david.123@localhost:5432/citric_elevator")
     # Read again after deletion
    all_states_after_deletion = manager.get_all_elevator_states()
    print("All states after deletion:", all_states_after_deletion)
    
    manager.delete_all_elevator_states()
    
    all_states_after_deletion = manager.get_all_elevator_states()
    print("All states after deletion:", all_states_after_deletion)
    
    
    
    # # Create
    # created_state = manager.create_elevator_state(current_floor=5, demand_floor=3,next_floor= 1,date_str="2023-12-21 08:30:00" )
    # print("Created state:", created_state)

    # # Read
    # all_states = manager.get_all_elevator_states()
    # print("All states:", all_states)

    # Update
    # manager.update_elevator_state_state(state_id=1, current_floor=8)
    # updated_state = manager.session.query(ElevatorState).filter_by(id=1).first()
    # print("Updated state:", updated_state)

    # Delete
    # manager.delete_elevator_state(state_id=1)