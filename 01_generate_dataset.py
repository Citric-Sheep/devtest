import sqlite3
import pandas as pd
from settings import DB_PATH, RAW_DATA_PATH

def fetch_data(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM elevator_calls", conn)
    conn.close()
    
    return df.dropna()
    


if __name__ == "__main__":
    df = fetch_data(DB_PATH)
    df.to_pickle(RAW_DATA_PATH)
