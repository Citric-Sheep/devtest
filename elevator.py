import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Path
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Session
from starlette import status
from models import ElevatorCall, Base
import pandas as pd
from database import engine, get_db


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/download_stats", status_code=status.HTTP_200_OK)
async def download_stats(db: Session = Depends(get_db)):
    """This endpoint will generate a CSV file under the 'stats' folder, with the database info

    Args:
        db (Session): Defaults to Depends(get_db).

    Returns:
        JSON: A message returning it generated the CSV file
    """
    df = pd.read_sql(sa.select(ElevatorCall), db.bind)
    df.to_csv(
        "stats/statistics.csv", columns=["call_time", "floor_number"], header=True
    )
    # I extract all the data to generate a CSV with all the elevator's calls made to date
    return {"CSV generated in stats folder"}


@app.get("/{floor}", status_code=status.HTTP_200_OK)
async def go_to_floor(
    floor: int = Path(default=..., ge=0, le=10),
    db: Session = Depends(get_db),
):
    """This endpoint will serve as the action of moving the elevator to a specific floor. You can't move to the same floor you're currently in

    Args:
        floor (int): The specific floor where the elevator will move to. Defaults to Path(default=..., ge=0, le=10).
        db (Session): Defaults to Depends(get_db).

    Returns:
        JSON: A message displaying the floor where you moved to.
    """
    last_call = db.query(ElevatorCall).order_by(ElevatorCall.id.desc()).first()
    if last_call is not None:
        if last_call.floor_number == floor:
            # In this case, the elevator does not move when I call it on the same floor
            return HTTPException(
                status_code=422, detail=f"You're already on floor #{floor}"
            )
    new_call = ElevatorCall(call_time=datetime.now(), floor_number=floor)
    db.add(new_call)
    db.commit()
    return {"message": f"You are now on floor #{floor}."}


@app.get("/")
async def base_api():
    return {"message": "This is a dev test for elevator challenge"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
