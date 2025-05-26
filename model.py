import pickle
import numpy as np
import pandas as pd
from settings import MODEL_PATH, FEATURES

class ElevetorModel:
    def __init__(self, model_path=MODEL_PATH):
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def compute_features(self, data_json):
        df = pd.DataFrame([data_json])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        df["weekday"] = df["timestamp"].dt.weekday
        df["day_name"] = df["timestamp"].dt.day_name()
        df["is_weekday"] = df["weekday"].isin([0,1,2,3,4]).astype(int)
        df["is_weekend"] = df["weekday"].isin([5,6]).astype(int)

        df["resting_floor"] = data_json.get("resting_floor", 1) 
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
        df["weekday_sin"] = np.sin(2 * np.pi * df["weekday"] / 7)
        df["weekday_cos"] = np.cos(2 * np.pi * df["weekday"] / 7)

        df["calls_from_calling_floor_last_5min"] = 0
        df["calls_from_calling_floor_last_hour"] = 0
        df["calls_from_calling_floor_last_day"] = 0
        df["calls_from_calling_floor_last_7_days"] = 0
        df["avg_time_between_calls_from_calling_floor"] = 0
        df["conditional_call_freq_given_resting_floor_last_7_days"] = 0
        df["conditional_call_freq_given_resting_floor_last_5_days"] = 0
        df["conditional_call_freq_given_resting_floor_last_24_hours"] = 0

        return df[FEATURES]

    def predict(self, data_json):
        features = self.compute_features(data_json)
        return int(self.model.predict(features)[0])

