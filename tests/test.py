"""
Run this file to execute tests
"""
import pytest
from dotenv import load_dotenv
from utils.db import PostgreSQLHandler


load_dotenv()


if __name__ == "__main__":
    """
    To run successfully the tests, the DB must be available. Tables will be created and populated automatically.
    After that, the update and deletion will also be tested. When all tests are passed, the tables will be erased.
    Take into account that this will create and erase the DB tables. If you want, tests can be done in a separate
    DB by changing the environment variable called DB_NAME. This will create and erase tables in a different DB
    without modifying any data. 
    """
    psql = PostgreSQLHandler()
    psql.init_db()
    pytest.main(['./'])
    psql.erase_tables()
