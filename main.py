"""
An entry point to get data from the database in a csv format, ready for use with pandas and timeseries.
"""
from fastapi import FastAPI
import os
from fastapi.responses import FileResponse
import psycopg2
import pandas as pd
from tempfile import NamedTemporaryFile


app = FastAPI()


@app.get("/get_data")
def get_data():
    connection = psycopg2.connect(
        database=f"{os.environ.get('POSTGRES_DB')}",
        user=f"{os.environ.get('POSTGRES_USER')}",
        password=f"{os.environ.get('POSTGRES_PASSWORD')}",
        host="my-database",
        port="5432"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM elevator_registry")

    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()
    df = pd.DataFrame(rows, columns=column_names)
    csv_data = df.to_csv(index=False)

    # Create a temporary file to store the CSV data
    with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        temp_file.write(csv_data)
        response = FileResponse(
            temp_file.name,
            filename="query_result.csv",
            headers={"Content-Type": "text/csv"}
        )

    return response
