##############
# Libraries #
##############

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from alembic.config import Config
from alembic import command

from apps.elevator.elevator_router import elevator_router

from database.db_utilities import db_connection
from database.db_models import BaseModel

from configuration import configuration

from .catalogs_data import catalog_data

###################
# Configuration #
###################

db_test_sqlalchemy_url = configuration.configure_bd_test_credentials.DB_URL
db_test_sqlalchemy_engine = create_engine(db_test_sqlalchemy_url)
metadata = MetaData()
db_test_sqlalchemy_session = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=db_test_sqlalchemy_engine)


def start_application():
    app = FastAPI()
    app.include_router(elevator_router)
    return app


#############################
# Database test functions #
############################

@pytest.fixture(scope="module")
def app():
    BaseModel.metadata.create_all(db_test_sqlalchemy_engine)
    db_session = db_test_sqlalchemy_session()

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes['configure_logger'] = False
    alembic_cfg.set_main_option("sqlalchemy.url", db_test_sqlalchemy_url)
    command.upgrade(alembic_cfg, "head")

    try:
        for table, data_list in catalog_data.items():
            for data in data_list:
                db_session.add(table(**data))
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print("Error: {}".format(e))
    finally:
        db_session.close()

    _app = start_application()
    yield _app
    BaseModel.metadata.drop_all(db_test_sqlalchemy_engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI):
    connection = db_test_sqlalchemy_engine.connect()
    transaction = connection.begin()
    session = db_test_sqlalchemy_session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: db_test_sqlalchemy_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[db_connection] = _get_test_db
    with TestClient(app) as client:
        yield client
