import io
from pathlib import Path
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from src.elevator import Elevator
from src.models import Demand
from src.mongo import read_all
from dotenv import load_dotenv 
import pandas as pd

dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path)

app = FastAPI()
elevator = Elevator()

'''
call endpoint
'''
@app.post('/call')
def call_elevator(demand : Demand) -> JSONResponse:
    result = elevator.process_demand(src_floor=demand.src_floor, 
                              dest_floor=demand.dest_floor,
                              load_weight=demand.weight 
                              ) 
    if 'error' in result:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error" : result['error']}  
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message" : result['message']}
    )

'''
formated_data endpoint
'''

@app.get('/formated_data')
def get_data() -> StreamingResponse:
    docs = read_all()

    if not docs:
        return StreamingResponse(
            iter(['No data available']),
            media_type='text/plain'
        )
    
    df = pd.DataFrame(docs)
    df['event_timestamp'] = df['start_timestamp'].combine_first(df['timestamp'])
    df.drop(columns=['start_timestamp', 'timestamp'], inplace=True)
    df.fillna("", inplace=True)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    csv_data = stream.getvalue()

    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=elevator_data.csv"}
    )