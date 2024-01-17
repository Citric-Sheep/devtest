from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from scr.crud_elevator import ElevatorStateManager
from scr.generate_dataset import GenerateDataset
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
from scr.db import Base
import uvicorn
import logging
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

inspector = inspect(engine)
if not inspector.has_table("elevator_state"):
    Base.metadata.create_all(bind=engine)

# Initialize ElevatorStateManager and GenerateDataset instances
elevator = ElevatorStateManager(database_url=DATABASE_URL)
generator = GenerateDataset()


@app.get("/run-generator")
async def run_generator():
    """Endpoint to run the elevator state generator.

    Returns:
        JSONResponse: A response indicating the success or failure of the generator execution.
    """
    try:
        generator.generate_elevator_states()
        return JSONResponse(
            content={"message": "Generator executed successfully"}, status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error running generator: {str(e)}"}, status_code=500
        )


@app.delete("/delete-all-rows")
async def delete_all_rows():
    """Endpoint to delete all elevator state rows from the database.

    Returns:
        JSONResponse: A response indicating the success or failure of the deletion operation.
    """
    try:
        elevator.delete_all_elevator_states()
        return JSONResponse(
            content={"message": "All rows deleted successfully"}, status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error deleting all rows: {str(e)}"}, status_code=500
        )


@app.get("/get-all-rows")
async def get_all_rows():
    """Endpoint to retrieve all elevator state rows from the database.

    Returns:
        JSONResponse: A response containing the retrieved rows or an error message.
    """
    try:
        all_rows = elevator.get_all_elevator_states()
        if not all_rows:
            all_rows = "No data in the database"
        return all_rows
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error getting all rows: {str(e)}"}, status_code=500
        )


@app.get("/save-to-csv")
async def save_to_csv(csv_filename: str = Query("elevator_states.csv")):
    """Endpoint to save all elevator state rows to a CSV file and allow users to download it.

    Args:
        csv_filename (str): The desired name for the CSV file.

    Returns:
        FileResponse: A response containing the CSV file for download or an error message.
    """
    try:
        all_rows = elevator.get_all_elevator_states()
        if not all_rows:
            return JSONResponse(
                content={"message": "No data in the database"}, status_code=500
            )

        # Convert rows to a DataFrame
        df = pd.DataFrame([row.__dict__ for row in all_rows])
        df = df.drop(columns=["_sa_instance_state"], errors="ignore")

        # Save DataFrame to a CSV file
        df.to_csv(csv_filename, index=False)

        # Use FileResponse to allow users to download the CSV file
        return FileResponse(csv_filename, filename=csv_filename, media_type="text/csv")
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error saving to CSV: {str(e)}"}, status_code=500
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
