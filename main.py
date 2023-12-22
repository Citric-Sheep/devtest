from fastapi import FastAPI, HTTPException,Query
from fastapi.responses import JSONResponse
from crud_elevator import ElevatorStateManager  # Assuming you have this module in the same directory
from generate_dataset import GenerateDataset  # Rename your existing code to generate_dataset.py
from sqlalchemy import create_engine, inspect
from fastapi.responses import StreamingResponse
import io
from dotenv import load_dotenv
from db import Base 
import uvicorn
import logging
import pandas as pd
import os


load_dotenv()

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

inspector = inspect(engine)
if not inspector.has_table("elevator_state"):
    Base.metadata.create_all(bind=engine)

elevator = ElevatorStateManager(database_url=DATABASE_URL)
generator = GenerateDataset()



@app.get("/run-generator")
async def run_generator():
    try:
        generator.generate_elevator_states()
        return JSONResponse(content={"message": "Generator executed successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Error running generator: {str(e)}"}, status_code=500)
    
@app.get("/delete-all-rows")
async def delete_all_rows():
    try:
        elevator.delete_all_elevator_states()
        return JSONResponse(content={"message": "All rows deleted successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"Error deleting all rows: {str(e)}"}, status_code=500)
    

@app.get("/get-all-rows")
async def get_all_rows():
    try:
        all_rows = elevator.get_all_elevator_states()
        if not all_rows:
            raise HTTPException(status_code=404, detail="No rows found in the database.")
        return all_rows
    except Exception as e:
        return JSONResponse(content={"message": f"Error getting all rows: {str(e)}"}, status_code=500)

@app.get("/save-to-csv")
async def save_to_csv(csv_filename: str = Query("elevator_states.csv")):
    try:
        all_rows = elevator.get_all_elevator_states()
        if not all_rows:
            raise HTTPException(status_code=404, detail="No rows found in the database.")

        # Convert rows to a DataFrame
        df = pd.DataFrame([row.__dict__ for row in all_rows])
        df = df.drop(columns=['_sa_instance_state'], errors='ignore')
        
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response
    except Exception as e:
        return JSONResponse(content={"message": f"Error saving to CSV: {str(e)}"}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info",reload = True)