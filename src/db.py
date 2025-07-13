import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# DB setup - using SQLite by default, but can override with env var
db_url = os.environ.get('DATABASE_URL', 'sqlite:///elevator_system.db')

# Set up SQLAlchemy stuff
engine = create_engine(db_url, echo=False)  # Set echo=True for debugging SQL
factory = sessionmaker(bind=engine)
Session = scoped_session(factory)

# This is used as the base class for all our models
Base = declarative_base()

# Create all the tables
def init_db():
    # Import models here to avoid circular imports
    from src.models import Building, Elevator, ElevatorCall, ElevatorTrip, ElevatorState, TimeStatistic, FloorStatistic
    Base.metadata.create_all(engine)
    print("DB initialized!")

# Helper for managing DB sessions
@contextmanager
def get_db_session():
    # Get a session, use it, then clean up properly
    s = Session()
    try:
        # Let the caller use the session
        yield s
        # Auto-commit if no exceptions
        s.commit()
    except Exception as e:
        # Something went wrong, rollback
        print(f"DB Error: {e}")
        s.rollback()
        raise
    finally:
        # Always close the session
        s.close()