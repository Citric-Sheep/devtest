import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(basedir, "instance", "elevator.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False