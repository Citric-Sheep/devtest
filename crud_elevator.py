from sqlalchemy import create_engine
from datetime import datetime
from models import ElevatorState
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from dotenv import load_dotenv
import os


# Create a session
class ElevatorStateManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_elevator_state(self, current_floor, demand_floor, next_floor, date_str):
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print("Invalid date format. Please provide a valid date.")
            return None

        if not all((current_floor, demand_floor, next_floor)):
            print(
                "Invalid input: current_floor, demand_floor, and next_floor cannot be None or empty."
            )
            return None

        new_state = ElevatorState(
            current_floor=current_floor,
            demand_floor=demand_floor,
            next_floor=next_floor,
            call_datetime=date,
        )
        self.session.add(new_state)
        self.session.commit()
        return new_state

    def get_last_elevator_state(self):
        if self.session.query(ElevatorState).count() == 0:
            print("No elevator states found in the database.")
            return None

        last_state = (
            self.session.query(ElevatorState).order_by(desc(ElevatorState.id)).first()
        )
        return last_state

    def get_all_elevator_states(self):
        return self.session.query(ElevatorState).all()

    def update_elevator_state_state(self, state_id, current_floor):
        if not state_id:
            print("Invalid input: state_id cannot be None or empty.")
            return None

        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            state.current_floor = current_floor
            self.session.commit()
            print(f"updated register with id={state_id}.")

            return state  # Return the updated state
        else:
            print(f"No state found with id={state_id}.")
        return None  # Return None if no state found

    def delete_elevator_state(self, state_id):
        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            self.session.delete(state)
            self.session.commit()
            print(f"deleted register with id={state_id}.")
        else:
            print(f"No state found with id={state_id}.")

    def delete_all_elevator_states(self):
        try:
            if self.session.query(ElevatorState).count() == 0:
                print("No elevator states found in the database.")
                return

            self.session.query(ElevatorState).delete()
            self.session.commit()
            print("All rows deleted successfully.")
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting all rows: {e}")


if __name__ == "__main__":
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    manager = ElevatorStateManager(database_url=DATABASE_URL)
    #  # Read again after deletion
    # all_states_after_deletion = manager.get_all_elevator_states()
    # print("All states after deletion:", all_states_after_deletion)

    # manager.delete_all_elevator_states()

    # all_states_after_deletion = manager.get_all_elevator_states()
    # print("All states after deletion:", all_states_after_deletion)

    # Create
    created_state = manager.create_elevator_state(
        current_floor=5, demand_floor=3, next_floor=1, date_str="2023-12-21 08:30:00"
    )
    print("Created state:", created_state)

    # Read
    all_states = manager.get_all_elevator_states()
    print("All states:", all_states)
    last_id = manager.get_last_elevator_state().id

    # Update
    manager.update_elevator_state_state(state_id=last_id, current_floor=8)
    updated_state = manager.session.query(ElevatorState).filter_by(id=1).first()

    # Delete
    manager.delete_elevator_state(state_id=last_id)
