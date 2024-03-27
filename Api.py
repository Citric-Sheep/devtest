from fastapi import FastAPI, HTTPException, Path, Query
from CRUD.CRUD import get_db_connection, create_trip, get_trips, update_trip, delete_trip


app = FastAPI()

@app.post("/trips/")
def create( start_time: str, end_time: str, is_demand: bool, start_floor: int= Query(..., ge=1, le=7), end_floor: int= Query(..., ge=1, le=7)):
    
    if start_floor < 1 or start_floor > 7 or end_floor < 1 or end_floor > 7:
        raise HTTPException(status_code=400, detail="Floor must be between 1 and 7")
    try:
        create_trip(start_floor, end_floor, start_time, end_time, is_demand)
        return {"message": "Trip created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trips/")
def read():
    try:
        trips = get_trips()
        return {"trips": trips}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/trips/{trip_id}/")
def update(trip_id: int, end_floor: int = Query(..., ge=1, le=7)):
    try:
        update_trip(trip_id, end_floor)
        return {"message": "Trip updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/trips/{trip_id}/")
def delete(trip_id: int):
    try:
        delete_trip(trip_id)
        return {"message": "Trip deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))