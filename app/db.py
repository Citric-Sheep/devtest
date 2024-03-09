from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql://ccastri:password@db:5432/elevator_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)


    
# Create a SessionLocal class to use for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()
