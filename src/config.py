from pydantic_settings import BaseSettings
from functools import lru_cache
import os

from dotenv import load_dotenv
load_dotenv('.env')


class BaseConfig(BaseSettings):
    TZ: str

    class Config:
        env_file = ".env"        

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_TEST_URI")

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_TEST_URI")
    #SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_HOMOLOG")}?charset=utf8mb4'                                                   

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_TEST_URI")
    #SQLALCHEMY_DATABASE_URI: str = f'mysql+pymysql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_PROD")}?charset=utf8mb4'

@lru_cache()
def get_settings():
    config_cls_dict = {
        "testing": TestingConfig,
        "development": DevelopmentConfig,
        "production": ProductionConfig
    }

    config_name = os.getenv("FASTAPI_CONFIG")
    config_cls = config_cls_dict[config_name]
    return config_cls()

settings = get_settings()