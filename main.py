"""
An entry point to get data from the database in a csv format, ready for use with pandas and timeseries.
"""
from fastapi import FastAPI
import os
from fastapi.responses import FileResponse
import psycopg2
import pandas as pd
import logging
from tempfile import NamedTemporaryFile


logger = logging.getLogger(__name__)


app = FastAPI()


# Replace with your database credentials
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

    # Execute a SELECT query
    cursor.execute("SELECT * FROM elevator_registry")

    # Fetch and process the results into a Pandas DataFrame
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    # Close the cursor and the connection
    cursor.close()
    connection.close()
    df = pd.DataFrame(rows, columns=column_names)
    csv_data = df.to_csv(index=False)

    logger.info("Data successfully retrieved from the database.")
    logger.debug(f"Data retrieved: {csv_data}")

    # Create a temporary file to store the CSV data
    with NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        temp_file.write(csv_data)
        response = FileResponse(
            temp_file.name,
            filename="query_result.csv",
            headers={"Content-Type": "text/csv"}
        )

    return response
