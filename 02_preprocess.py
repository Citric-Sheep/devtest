import pandas as pd
import numpy as np
from settings import RAW_DATA_PATH, PROCESSED_DATA_PATH
from tqdm import tqdm

def basic_time_features(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.weekday
    df["day_name"] = df["timestamp"].dt.day_name()
    df["is_weekday"] = df["weekday"].isin([0,1,2,3,4])
    df["is_weekend"] = df["weekday"].isin([5,6])
    df["resting_floor"] = df["calling_floor"].shift(1)
    return df

def cyclical_features(df):
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["weekday_sin"] = np.sin(2 * np.pi * df["weekday"] / 7)
    df["weekday_cos"] = np.cos(2 * np.pi * df["weekday"] / 7)
    df.drop(columns=["hour", "weekday"], inplace=True)
    return df

def rolling_floor_features(df):
    df["calls_from_calling_floor_last_5min"] = 0
    df["calls_from_calling_floor_last_hour"] = 0
    df["calls_from_calling_floor_last_day"] = 0
    df["calls_from_calling_floor_last_7_days"] = 0
    df["avg_time_between_calls_from_calling_floor"] = np.nan

    for floor in tqdm(df["calling_floor"].unique(), desc="Rolling features by floor"):
        mask = df["calling_floor"] == floor
        floor_df = df.loc[mask].copy()
        floor_df = floor_df.set_index("timestamp")
        floor_df = floor_df.sort_index()

        calls_last_5min = floor_df.rolling("5min").count()["calling_floor"] - 1
        calls_last_hour = floor_df.rolling("1h").count()["calling_floor"] - 1
        calls_last_day = floor_df.rolling("1d").count()["calling_floor"] - 1
        calls_last_7_days = floor_df.rolling("7d").count()["calling_floor"] - 1
        avg_time_between_calls = floor_df.index.to_series().diff().dt.total_seconds().rolling(10, min_periods=1).mean()

        idx = df.index[mask]
        df.loc[idx, "calls_from_calling_floor_last_5min"] = calls_last_5min.values
        df.loc[idx, "calls_from_calling_floor_last_hour"] = calls_last_hour.values
        df.loc[idx, "calls_from_calling_floor_last_day"] = calls_last_day.values
        df.loc[idx, "calls_from_calling_floor_last_7_days"] = calls_last_7_days.values
        df.loc[idx, "avg_time_between_calls_from_calling_floor"] = avg_time_between_calls.values
    return df

def conditional_freq_given_resting_floor(df):
    df["conditional_call_freq_given_resting_floor_last_7_days"] = 0
    df["conditional_call_freq_given_resting_floor_last_5_days"] = 0
    df["conditional_call_freq_given_resting_floor_last_24_hours"] = 0

    for i, row in tqdm(df.iterrows(), total=len(df), desc="Conditional freq given resting floor"):
        curr_time = row["timestamp"]
        curr_calling_floor = row["calling_floor"]
        curr_resting_floor = row["resting_floor"]

        mask_time_7d = (df["timestamp"] < curr_time) & (df["timestamp"] >= curr_time - pd.Timedelta(days=7))
        mask_resting = (df["resting_floor"] == curr_resting_floor)
        mask_calling = (df["calling_floor"] == curr_calling_floor)
        df.loc[i, "conditional_call_freq_given_resting_floor_last_7_days"] = df.loc[mask_time_7d & mask_resting & mask_calling].shape[0]

        mask_time_5d = (df["timestamp"] < curr_time) & (df["timestamp"] >= curr_time - pd.Timedelta(days=5))
        df.loc[i, "conditional_call_freq_given_resting_floor_last_5_days"] = df.loc[mask_time_5d & mask_resting & mask_calling].shape[0]

        mask_time_24h = (df["timestamp"] < curr_time) & (df["timestamp"] >= curr_time - pd.Timedelta(hours=24))
        df.loc[i, "conditional_call_freq_given_resting_floor_last_24_hours"] = df.loc[mask_time_24h & mask_resting & mask_calling].shape[0]

    return df

def preprocess(df):
    df = basic_time_features(df)
    df = cyclical_features(df)
    df = rolling_floor_features(df)
    df = conditional_freq_given_resting_floor(df)
    for col in df.select_dtypes(bool).columns:
        df[col] = df[col].astype(int)

    df = df.iloc[1:].reset_index(drop=True)
    df.fillna(0, inplace=True)
    return df

if __name__ == "__main__":
    df = pd.read_pickle(RAW_DATA_PATH)
    df = df.rename(columns={"from_floor": "calling_floor"})
    df_processed = preprocess(df)
    df_processed.to_pickle(PROCESSED_DATA_PATH)
