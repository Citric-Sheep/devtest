"""
In this file you'll find a PostgreSQL handler. This class is intended to handle connection
"""
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable
from models.models import Base
from typing import Any

TABLES = ["buildings", "elevators", "demands"]


class PostgreSQLHandler:
    """
    Class in charge of handling DB operations such as create, read, update and delete.
    """
    def __init__(self):
        url = (
            f'postgresql://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@'
            f'{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
        )
        self.engine = create_engine(url)
        self.session = sessionmaker(self.engine)()
        self._inspector = inspect(self.engine)

    def _create_table(self, table_name, base: Any = None):
        if not self._inspector.has_table(table_name):
            metadata = Base.metadata if not base else base.metadata
            table_obj = metadata.tables.get(table_name)
            if table_obj is not None:
                with self.engine.connect() as connection:
                    connection.execute(CreateTable(table_obj))
                    connection.commit()
                print(f"Table {table_name} created successfully.")
            else:
                print(f"Error: Table {table_name} definition not found.")
        else:
            print(f"Table {table_name} already exists.")

    def erase_tables(self):
        metadata = Base.metadata
        self.session.close_all()
        print("Session closed, erasing tables...")
        metadata.drop_all(self.engine, [metadata.tables.get(table) for table in TABLES[::-1]], checkfirst=True)
        print("Tables erased")

    def init_db(self):
        for table in TABLES:
            self._create_table(table)

    def create(self, obj: object) -> str:
        try:
            self.session.add(obj)
            self.session.commit()
            return "Success"
        except SQLAlchemyError as e:
            return str(e.__dict__['orig'])

    def read(self, obj: object, filter_by: dict = None) -> list:
        if filter_by:
            query = self.session.query(obj).filter_by(**filter_by).all()
        else:
            query = self.session.query(obj).all()
        return query

    def update(self, obj: object, filter_by: dict, values: dict) -> str:
        try:
            query = self.read(obj, filter_by)
            if not query:
                return "No matching records found for update"
            # Accessing 0 position because of a prior filter with ID. It shouldn't return more than one element
            for key, value in values.items():
                setattr(query[0], key, value)
            self.session.commit()
            return "Success"
        except SQLAlchemyError as e:
            return str(e.__dict__['orig'])

    def delete(self, obj: object, filter_by: dict = None) -> str:
        try:
            query = self.read(obj, filter_by)
            if not query:
                return "No matching records found for delete"

            self.session.delete(query[0])
            self.session.commit()
            return "Success"
        except SQLAlchemyError as e:
            return str(e.__dict__['orig'])
