DB_PATH = "db/elevator_calls.sqlite"
RAW_DATA_PATH = "artifacts/data/raw_data.pkl"
PROCESSED_DATA_PATH = "artifacts/data/processed_data.pkl"
MODEL_PATH = "artifacts/models/model.pkl"

FEATURES = [
    "calling_floor",
    "resting_floor",
    "hour_sin", "hour_cos", "weekday_sin", "weekday_cos",
    "calls_from_calling_floor_last_5min",
    "calls_from_calling_floor_last_hour",
    "calls_from_calling_floor_last_day",
    "calls_from_calling_floor_last_7_days",
    "avg_time_between_calls_from_calling_floor",
    "conditional_call_freq_given_resting_floor_last_7_days",
    "conditional_call_freq_given_resting_floor_last_5_days",
    "conditional_call_freq_given_resting_floor_last_24_hours",
    "is_weekday",
    "is_weekend"
]
TARGET = "calling_floor"
TEST_SIZE = 0.2
RANDOM_STATE = 42