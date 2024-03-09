import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# Database configuration for localhost
# DATABASE_URL = f"postgresql://ccastri:password@localhost:5432/elevator_db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class to use for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()
