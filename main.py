import uvicorn
import pandas as pd

from src import get_db, ElevatorCall
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

FIRST_FLOOR = 1


# Endpoint to simulate elevator call (demand creation)
@app.post('/call-elevator')
async def call_elevator(request: dict, db: Session = Depends(get_db)):
    """Simulates a call for the elevator

    Args:
        target_floor (int): The requested floor to go to
        db (Session, optional): The database session
    Returns:
        dict: A response message with the status of the call
    """
    elevator = db.query(ElevatorCall).order_by(ElevatorCall.id.desc()).first()
    elevator = ElevatorCall(target_floor=request["target_floor"],
                            current_floor=elevator.target_floor
                            if elevator is not None else FIRST_FLOOR,
                            user_floor=request["user_floor"],
                            timestamp=datetime.now())
    db.add(elevator)
    db.commit()
    return JSONResponse({"message": "Elevator called successfully"},
                        status_code=200)


@app.get('/get-elevator-calls')
async def get_elevator_calls(db: Session = Depends(get_db)):
    """
    Retrieves a list of all elevator calls from the database.

    Args:
        db (Session, optional): The database session. Automatically injected by FastAPI.

    Returns:
        JSONResponse: A response containing the retrieved elevator call data.
            - If calls exist, returns a JSON response with a success message and the data.
            - If no calls exist, returns a JSON response indicating that the elevator has not been called yet.
    """
    elevators = db.query(ElevatorCall).all()
    if elevators:
        return JSONResponse(
            {
                "message": "Calls retrieved succesfully",
                "data": jsonable_encoder(elevators)
            },
            status_code=200)
    else:
        return JSONResponse({"message": "Elevator has not been called yet"},
                            status_code=200)


@app.delete('/reset-elevator')
async def reset_elevator(db: Session = Depends(get_db)):
    if db.query(ElevatorCall).count() == 0:
        return JSONResponse({"message": "Elevator has not been called yet"},
                            status_code=200)
    db.query(ElevatorCall).delete()
    db.commit()
    return JSONResponse({"message": "Elevator reset successfully"},
                        status_code=200)


@app.get('/get-last-call')
async def get_last_call(db: Session = Depends(get_db)):
    """
    Resets the elevator system by deleting all recorded elevator calls from the database.

    Args:
        db (Session, optional): The database session. Automatically injected by FastAPI.

    Returns:
        JSONResponse: A response indicating the success of the elevator reset.
            - If no calls exist, returns a JSON response indicating that the elevator has not been called yet.
            - If calls exist, deletes all calls, commits the changes, and returns a success message.
    """
    elevator = db.query(ElevatorCall).order_by(ElevatorCall.id.desc()).first()
    if elevator:
        return JSONResponse(
            {
                "call": jsonable_encoder(elevator),
                "message": "Last call succesfully retrieved"
            },
            status_code=200)
    else:
        return JSONResponse({"message": "Elevator has not been called yet"},
                            status_code=200)


@app.get('/get-data-csv', response_class=FileResponse)
async def get_data_csv(db: Session = Depends(get_db)):
    """
    Retrieves elevator call data from the database and exports it to a CSV file.

    Args:
        db (Session, optional): The database session. Automatically injected by FastAPI.

    Returns:
        FileResponse or JSONResponse: 
            - If calls exist, exports the data to a CSV file and returns the file as a response.
            - If no calls exist, returns a JSON response indicating that the elevator has not been called yet.
    """
    elevators = db.query(ElevatorCall).all()
    df = pd.DataFrame([elevator.__dict__ for elevator in elevators])
    df.drop(columns=['_sa_instance_state'], inplace=True)
    df.to_csv('data.csv', index=False)
    if elevators:
        return FileResponse('data.csv', media_type='text/csv')
    else:
        return JSONResponse({"message": "Elevator has not been called yet"},
                            status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
