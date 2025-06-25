from fastapi import APIRouter, HTTPException
from app.schemas.model_input import RestingFloorRequest
import joblib
import numpy as np
import os

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../../ml/resting_floor_model.joblib")
model = joblib.load(MODEL_PATH)

@router.post("/predict_resting_floor/")
def predict_resting_floor(request: RestingFloorRequest):
    try:
        features = [
            request.hour,
            request.weekday,
            request.demand_count,
            request.avg_floor,
            request.most_common_floor,
            request.avg_direction,
            request.peak_hours
        ]
        pred = model.predict([features])[0]
        return {"best_resting_floor": int(pred)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
