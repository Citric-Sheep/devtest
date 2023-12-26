from sqlalchemy import create_engine
from datetime import datetime
from scr.models import ElevatorState
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from dotenv import load_dotenv
import os

class ElevatorStateManager:
    """Manages the state of elevators and interacts with the database.

    Args:
        database_url (str): The URL of the database.

    Attributes:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.
        Session (sqlalchemy.orm.session.sessionmaker): The SQLAlchemy session maker.
        session (sqlalchemy.orm.session.Session): The current SQLAlchemy session.
    """

    def __init__(self, database_url):
        """Initializes the ElevatorStateManager.

        Args:
            database_url (str): The URL of the database.
        """
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_elevator_state(self, current_floor, demand_floor, next_floor, date_str):
        """Creates a new elevator state and adds it to the database.

        Args:
            current_floor (int): The current floor of the elevator.
            demand_floor (int): The floor where the elevator is in demand.
            next_floor (int): The next floor the elevator will move to.
            date_str (str): A string representing the date and time in the format "%Y-%m-%d %H:%M:%S".

        Returns:
            ElevatorState: The newly created ElevatorState object, or None if creation fails.
        """
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
        """Retrieves the last recorded elevator state from the database.

        Returns:
            ElevatorState: The last recorded ElevatorState object, or None if no states are found.
        """
        if self.session.query(ElevatorState).count() == 0:
            print("No elevator states found in the database.")
            return None

        last_state = (
            self.session.query(ElevatorState).order_by(desc(ElevatorState.id)).first()
        )
        return last_state

    def get_all_elevator_states(self):
        """Retrieves all elevator states from the database.

        Returns:
            list: A list of ElevatorState objects.
        """
        return self.session.query(ElevatorState).all()

    def update_elevator_state_state(self, state_id, current_floor):
        """Updates the current floor of a specific elevator state.

        Args:
            state_id (int): The ID of the elevator state to update.
            current_floor (int): The new current floor value.

        Returns:
            ElevatorState: The updated ElevatorState object, or None if the state is not found.
        """
        if not state_id:
            print("Invalid input: state_id cannot be None or empty.")
            return None

        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            state.current_floor = current_floor
            self.session.commit()
            print(f"Updated register with id={state_id}.")
            return state
        else:
            print(f"No state found with id={state_id}.")
        return None

    def delete_elevator_state(self, state_id):
        """Deletes a specific elevator state from the database.

        Args:
            state_id (int): The ID of the elevator state to delete.
        """
        state = self.session.query(ElevatorState).filter_by(id=state_id).first()
        if state:
            self.session.delete(state)
            self.session.commit()
            print(f"Deleted register with id={state_id}.")
        else:
            print(f"No state found with id={state_id}.")

    def delete_all_elevator_states(self):
        """Deletes all elevator states from the database."""
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
